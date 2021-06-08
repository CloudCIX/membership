"""
Management of links between Addresses
"""

# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

# local
from membership.controllers import (
    AddressLinkCreateController,
    AddressLinkUpdateController,
)
from membership.models import Address, AddressLink
from membership.permissions.address_link import Permissions
from membership.serializers import AddressLinkSerializer

__all__ = [
    'AddressLinkResource',
]


class AddressLinkResource(APIView):

    def post(self, request: Request, address_id: int) -> Response:
        """
        summary: Create a new link between two Addresses

        description: |
            This method creates a link between the Address specified with `address_id` and the Address of the User
            making the request.

            These links are required in order to carry out transactions between Addresses.

        path_params:
            address_id:
                description: The id of the other Address to which a link will be created
                type: integer

        responses:
            201:
                description: Address link successfully created
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_contra_address_object', child_of=request.span):
            try:
                contra_address = Address.objects.get(pk=address_id)
            except Address.DoesNotExist:
                return Http404(error_code='membership_address_link_create_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request, contra_address)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AddressLinkCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('retrieving_user_address_object', child_of=request.span):
            address = Address.objects.get(pk=request.user.address['id'])
            controller.instance.address = address
            controller.instance.contra_address = contra_address

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        # Create the opposite link if it does not exist
        with tracer.start_span('get_or_create_reverse_link', child_of=request.span) as span:
            try:
                AddressLink.objects.get(
                    address=contra_address,
                    contra_address=address,
                )
                span.set_tag('action', 'get')  # pragma: no cover
            except AddressLink.DoesNotExist:
                AddressLink.objects.create(address=contra_address, contra_address=address, reference='')
                span.set_tag('action', 'create')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AddressLinkSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)

    def get(self, request: Request, address_id: int) -> Response:
        """
        summary: Read the details of an Address Link

        description: |
            Address Links can be used to store notes about other Addresses that you are linked to.
            This method allows a User to read the details of the link between their Address and the Address specified
            with `address_id`

        path_params:
            address_id:
                description: The id of the other Address in the link to be read
                type: integer

        responses:
            200:
                description: Address link was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = AddressLink.objects.get(address_id=request.user.address['id'], contra_address_id=address_id)
            except AddressLink.DoesNotExist:
                return Http404(error_code='membership_address_link_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AddressLinkSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, address_id: int, partial=False) -> Response:
        """
        summary: Update the details of an Address Link

        description: |
            Address Links can be used to store notes about other Addresses that you are linked to.
            This method allows a User to update the details of the link between their Address and the Address specified
            with `address_id`

        path_params:
            address_id:
                description: The id of the other Address in the link to be updated
                type: integer

        responses:
            200:
                description: Address link was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = AddressLink.objects.get(address_id=request.user.address['id'], contra_address_id=address_id)
            except AddressLink.DoesNotExist:
                return Http404(error_code='membership_address_link_update_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AddressLinkUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AddressLinkSerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, address_id: int) -> Response:
        """
        Attempt to partially update an Address Link record
        """
        return self.put(request, address_id, True)
