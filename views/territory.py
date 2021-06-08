"""
Manage a Member's Territory records
"""

# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import (
    TerritoryCreateController,
    TerritoryListController,
    TerritoryUpdateController,
)
from membership.models import Territory
from membership.permissions.territory import Permissions
from membership.serializers import TerritorySerializer


__all__ = [
    'TerritoryCollection',
    'TerritoryResource',
]


class TerritoryCollection(APIView):
    """
    Handles methods regarding Territory records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Territory records

        description: |
            Retrieve a list of Territory records for the requesting User's Member.

            A Territory is a classification or tag that a Member can use for grouping their business partners.
            For example, a Member can group business partners by location, or by what product they purchase.

        responses:
            200:
                description: A list of Territory records, filtered and ordered by the User
        """
        tracer = settings.TRACER

        # Validate the user filters
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = TerritoryListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        # Get the objects
        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            order = controller.cleaned_data['order']
            objs = Territory.objects.filter(
                member_id=request.user.member['id'],
                **controller.cleaned_data['search'],
            ).exclude(
                **controller.cleaned_data['exclude'],
            ).order_by(
                order,
            )

        # Gather the metadata
        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            warnings = controller.warnings
            metadata = {
                'page': page,
                'limit': limit,
                'order': order,
                'total_records': total_records,
                'warnings': warnings,
            }
            # Pagination
            objs = objs[page * limit:(page + 1) * limit]

        # Generate and return the Response
        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = TerritorySerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Territory record

        description: |
            Create a new Territory record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Territory record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        # Check permissions for creation
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        # Validate the User data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = TerritoryCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        # Save the instance
        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        # Generate and return the response
        with tracer.start_span('serializing_data', child_of=request.span):
            data = TerritorySerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class TerritoryResource(APIView):
    """
    Handles methods regarding territory records that do require an id to be specified, i.e. read, update, delete
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Territory record

        description: |
            Attempt to read a Territory record in the requesting User's Member by the given `pk`, returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Territory record to be read
                type: integer

        responses:
            200:
                description: Territory record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        # Try to get the Territory object
        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Territory.objects.get(id=pk, member_id=request.user.member['id'])
            except Territory.DoesNotExist:
                return Http404(error_code='membership_territory_read_001')

        # Generate and return a response
        with tracer.start_span('serializing_data', child_of=request.span):
            data = TerritorySerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Territory record

        description: |
            Attempt to update a Territory record in the requesting User's Member by the given `pk`, returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Territory record to be updated
                type: integer

        responses:
            200:
                description: Territory record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        # Check permissions
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request)
            if err is not None:
                return err

        # Try to get the Territory object
        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Territory.objects.get(id=pk, member_id=request.user.member['id'])
            except Territory.DoesNotExist:
                return Http404(error_code='membership_territory_update_001')

        # Validate the User data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = TerritoryUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        # Save the updated data
        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        # Generate and return the response
        with tracer.start_span('serializing_data', child_of=request.span):
            data = TerritorySerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Territory record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int) -> Response:
        """
        summary: Delete a specified Territory record

        description: |
            Attempt to delete a Territory record in the requesting User's Member by the given `pk`, returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Territory record to delete
                type: integer

        responses:
            204:
                description: Territory record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        # Try to get the Territory object
        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Territory.objects.get(pk=pk, member_id=request.user.member['id'])
            except Territory.DoesNotExist:
                return Http404(error_code='membership_territory_delete_001')

        # Check Permissions
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        # Delete the object and return
        with tracer.start_span('saving_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
