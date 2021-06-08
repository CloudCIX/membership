"""
Read-only services for Country data
"""

# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import CountryListController
from membership.models import Country
from membership.serializers import CountrySerializer


__all__ = [
    'CountryCollection',
    'CountryResource',
]


class LoginPermission(BasePermission):
    """
    Custom DRF Permission for this class
    """
    def has_permission(self, request, view):
        return True


class CountryCollection(APIView):
    """
    Handles methods regarding Country records that do not require an id to be specified, i.e. list, create
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Country records

        description: |
            Retrieves a list of Country records, including their ISO 3166 codes

        responses:
            200:
                description: A list of Country records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CountryListController(data=request.GET, request=request, span=span)
            # By validating the controller we will generate the filters
            controller.is_valid()

        # Now get a list of Country records using the filters
        with tracer.start_span('get_objects', child_of=request.span):
            try:
                # Search and exclude can be empty dicts so there's no need to check
                # if they're populated
                objs = Country.objects.filter(
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='membership_country_list_001')

        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            order = controller.cleaned_data['order']
            limit = controller.cleaned_data['limit']
            warnings = controller.warnings
            metadata = {
                'total_records': total_records,
                'page': page,
                'limit': limit,
                'order': order,
                'warnings': warnings,
            }
            # Handle pagination
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = CountrySerializer(instance=objs, many=True).data

        # Generate and return response
        return Response({'content': data, '_metadata': metadata})


class CountryResource(APIView):
    """
    Handles methods regarding Country records that do require an id to be specified, i.e. read
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Country record

        description: |
            Attempt to read a Country record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Country record to be read
                type: integer

        responses:
            200:
                description: Country record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Country.objects.get(id=pk)
            except Country.DoesNotExist:
                return Http404(error_code='membership_country_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CountrySerializer(instance=obj).data

        return Response({'content': data})
