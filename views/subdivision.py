"""
Read-only services for data on Subdivisions of Countries supported by CloudCIX
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
from membership.controllers import SubdivisionListController
from membership.models import Country, Subdivision
from membership.serializers import SubdivisionSerializer


__all__ = [
    'SubdivisionCollection',
    'SubdivisionResource',
]


class LoginPermission(BasePermission):
    """
    Custom DRF Permission for this class
    """
    def has_permission(self, request, view):
        return True


class SubdivisionCollection(APIView):
    """
    Handles methods regarding Subdivision records that do not require an id to be specified -> list
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request, country_id: int) -> Response:
        """
        summary: Retrieve a list of Subdivision records

        description: |
            Retrieve a list of Subdivision records for a given Country, along with their ISO 3166-2 codes

        path_params:
            country_id:
                description: The id of the Country to fetch Subdivision records for
                type: integer

        responses:
            200:
                description: A list of Subdivision records, filtered and ordered by the User
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_country_object', child_of=request.span):
            try:
                country = Country.objects.get(id=country_id)
            except Country.DoesNotExist:
                return Http404(error_code='membership_subdivision_list_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = SubdivisionListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            order = controller.cleaned_data['order']
            # Get the subdivision records, including the user filters
            try:
                objs = Subdivision.objects.filter(
                    country=country,
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    order,
                )
            except (ValueError, ValidationError):
                return Http400(error_code='membership_subdivision_list_002')

        # Gather metadata
        # Only create vars for things we use more than once (efficiency)
        # or that we need to save
        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            # Handle pagination
            objs = objs[page * limit:(page + 1) * limit]
            # Generate response data
            metadata = {
                'total_records': total_records,
                'page': page,
                'limit': limit,
                'order': order,
                'warnings': controller.warnings,
            }

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = SubdivisionSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})


class SubdivisionResource(APIView):
    """
    Handles methods regarding Subdivision records that do require an id to be specified -> read
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request, country_id: int, pk: int) -> Response:
        """
        summary: Read the details of a specified Subdivision record

        description: |
            Attempt to read a Subdivision record in the specified Country by the given `pk`,
            returning a 404 if it or the Country does not exist

        path_params:
            country_id:
                description: The id of the Country to fetch Subdivision records for
                type: integer
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
                obj = Subdivision.objects.get(country_id=country_id, id=pk)
            except Subdivision.DoesNotExist:
                return Http404(error_code='membership_subdivision_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = SubdivisionSerializer(instance=obj).data

        return Response({'content': data})
