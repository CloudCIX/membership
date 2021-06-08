"""
Read-only services for data on Currencies supported by CloudCIX
"""

# libs
from cloudcix_rest.exceptions import Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import CurrencyListController
from membership.models import Currency
from membership.serializers import CurrencySerializer

__all__ = [
    'CurrencyCollection',
    'CurrencyResource',
]


class LoginPermission(BasePermission):
    """
    Custom DRF Permission for this class
    """
    def has_permission(self, request, view):
        return True


class CurrencyCollection(APIView):
    """
    Handles the getting of a list of currencies supported by CIX
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Currency records

        description: |
            Retrieve a list of all of the Currencies that are supported by the CloudCIX platform

        responses:
            200:
                description: A list of Currency records, filtered and ordered by the User
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CurrencyListController(data=request.GET, request=request, span=span)
            # By validating the controller we will generate the filters
            controller.is_valid()

        # Now get a list of Currency records using the filters
        # Search and exclude can be empty dicts so there's no need to check
        # if they're populated
        # Only character fields so ValidationErrors can't be thrown
        with tracer.start_span('get_objects', child_of=request.span):
            objs = Currency.objects.filter(
                **controller.cleaned_data['search'],
            ).exclude(
                **controller.cleaned_data['exclude'],
            ).order_by(
                controller.cleaned_data['order'],
            )

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
            # Pagination
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = CurrencySerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})


class CurrencyResource(APIView):
    """
    Handles the getting the details of a currency
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Currency record

        description: |
            Attempt to read an Currency record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Currency record to be read
                type: integer

        responses:
            200:
                description: Currency record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Currency.objects.get(id=pk)
            except Currency.DoesNotExist:
                return Http404(error_code='membership_currency_read_001')

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            data = CurrencySerializer(instance=obj).data

        return Response({'content': data})
