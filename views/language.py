"""
Read-only services for data on Languages supported by CloudCIX
"""

# libs
from cloudcix_rest.exceptions import Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import LanguageListController
from membership.models import Language
from membership.serializers import LanguageSerializer


__all__ = [
    'LanguageCollection',
    'LanguageResource',
]


class LoginPermission(BasePermission):
    """
    Custom DRF Permission for this class
    """
    def has_permission(self, request, view):
        return True


class LanguageCollection(APIView):
    """
    Handles methods regarding Language records that do not require an id to be specified, i.e. list, create
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Language records

        description: |
            Retrieve a list of all of the Languages that are supported by the CloudCIX platform

        responses:
            200:
                description: A list of Language records, filtered and ordered by the User
        """
        tracer = settings.TRACER

        # Create a controller to validate the user data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = LanguageListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        # Try to use the filters
        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            order = controller.cleaned_data['order']
            # Only char fields, so no validation errors can be thrown
            objs = Language.objects.filter(
                **controller.cleaned_data['search'],
            ).exclude(
                **controller.cleaned_data['exclude'],
            ).order_by(
                order,
            )

        # Generate the metadata
        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
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

        # Generate and return response
        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = LanguageSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})


class LanguageResource(APIView):
    """
    Handles methods regarding Language records that do require an id to be specified, i.e. read, update, delete
    """

    permission_classes = (LoginPermission,)

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Language record

        description: |
            Attempt to read a Language record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Language record to be read
                type: integer

        responses:
            200:
                description: Language record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Language.objects.get(id=pk)
            except Language.DoesNotExist:
                return Http404(error_code='membership_language_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = LanguageSerializer(instance=obj).data

        return Response({'content': data})
