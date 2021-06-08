"""
Management of Addresses
"""

# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from cloudcix_metrics import prepare_metrics, Metric
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import BooleanField, Prefetch, Value
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import (
    AddressCreateController,
    AddressListController,
    AddressUpdateController,
)
from membership.models import Address, AddressLink
from membership.permissions.address import Permissions
from membership.serializers import AddressSerializer


__all__ = [
    'AddressCollection',
    'AddressResource',
    'VerboseAddressCollection',
]


class AddressCollection(APIView):
    """
    Handles methods regarding Address records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Address records

        description: |
            Retrieve a list of Address records that the requesting User is linked to.

        responses:
            200:
                description: A list of Address records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        # Create a list controller to parse user data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AddressListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        kw = controller.cleaned_data['search']
        order = controller.cleaned_data['order']
        with tracer.start_span('get_objects', child_of=request.span) as span:
            try:
                with tracer.start_span('get_linked_address_ids', child_of=span):
                    # Get the addresses that are linked to the User's for listing
                    linked_address = set(AddressLink.objects.filter(
                        address_id=request.user.address['id'],
                    ).values_list(
                        'contra_address_id',
                        flat=True,
                    ))
                    if kw.get('id__in', False):
                        id_set = {int(i) for i in kw['id__in']}
                        kw['id__in'] = id_set & linked_address
                    else:
                        kw['id__in'] = linked_address

                with tracer.start_span('checking_search_filters', child_of=span):
                    # If the User is filtering by the Address Link table, we want to make sure they only filter on
                    # Address Links where Address id belongs to their own Address
                    address_required = False
                    for key in (*kw.keys(), *controller.cleaned_data['exclude'].keys()):
                        if key.startswith('address_link'):
                            address_required = True
                            break

                    if address_required:
                        kw['address_link__address_id'] = request.user.address['id']

                with tracer.start_span('retrieve_requested_objects', child_of=span):
                    # Get the list of Address objects
                    objs = Address.objects.filter(
                        **kw,
                    ).exclude(
                        **controller.cleaned_data['exclude'],
                    ).order_by(
                        *controller.cleaned_data['order'],
                    ).annotate(linked=Value(True, BooleanField()))
            except (ValueError, ValidationError):
                return Http400(error_code='membership_address_list_001')

        # Gather metadata
        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            warnings = controller.warnings
            # Get a string version of the order to return in the metadata
            meta_order = order[0] if len(order) == 1 else 'full_address' if '-' not in order[0] else '-full_address'
            metadata = {
                'page': page,
                'limit': limit,
                'order': meta_order,
                'total_records': total_records,
                'warnings': warnings,
            }
            # Pagination
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = AddressSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Address record

        description: |
            Create a new Address record using the data supplied by the User.

        responses:
            201:
                description: Address record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        # Validate the user data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AddressCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)
        member = controller.instance.member

        # Check the permission
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request, member)
            if err is not None:
                return err

        # Save the Address object
        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        # Create the necessary links
        # Self link
        with tracer.start_span('creating_self_link', child_of=request.span):
            AddressLink.objects.create(
                address=controller.instance,
                contra_address=controller.instance,
                reference='Self Link',
            )

        # Link the new address to the user's address
        with tracer.start_span('creating_user_address_links', child_of=request.span):
            link = AddressLink.objects.create(address_id=request.user.address['id'], contra_address=controller.instance)
            AddressLink.objects.create(address=controller.instance, contra_address_id=request.user.address['id'])
            # Serialize the link
            controller.instance.link = link
            controller.instance.linked = True

        # Send a metric to indicate an Address record has been created
        prepare_metrics(lambda pk: Metric('address_create', pk, {}), pk=controller.instance.pk)

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AddressSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class AddressResource(APIView):
    """
    Handles methods regarding Address records that require an id to be specified, i.e. read, update, delete
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Address record

        description: |
            Attempt to read an Address record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Address record to be read
                type: integer

        responses:
            200:
                description: Address record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Address.objects.get(id=pk)
            except Address.DoesNotExist:
                return Http404(error_code='membership_address_read_001')

        # Check perms for the user and object
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        # Set link between the chosen address and the user's address
        with tracer.start_span('retrieving_address_link_object', child_of=request.span) as span:
            try:
                obj.link = AddressLink.objects.get(address_id=request.user.address['id'], contra_address=obj)
                span.set_tag('found', 'yes')
            except AddressLink.DoesNotExist:  # pragma: no cover
                # Won't happen in tests, happens rarely on stage
                span.set_tag('found', 'no')
                obj.link = None
            obj.linked = obj.link is not None

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AddressSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Address record

        description: |
            Attempt to update an Address record by the given `pk`, returning a 404 if it does not exist.

        path_params:
            pk:
                description: The id of the Address record to be updated
                type: integer

        responses:
            200:
                description: Address record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Address.objects.get(id=pk)
            except Address.DoesNotExist:
                return Http404(error_code='membership_address_update_001')

        # Save some of the original address data
        current_cloud_region = obj.cloud_region

        # Create the controller to handle user input
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AddressUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        # Check permissions
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request, obj, current_cloud_region, controller.instance.cloud_region)
            if err is not None:
                return err

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('retrieving_address_link_object', child_of=request.span) as span:
            try:
                controller.instance.link = AddressLink.objects.get(
                    address_id=request.user.address['id'],
                    contra_address=obj,
                )
                span.set_tag('found', 'yes')
            except AddressLink.DoesNotExist:  # pragma: no cover
                # Won't happen in tests, happens rarely on stage
                span.set_tag('found', 'no')
                controller.instance.link = None
            controller.instance.linked = controller.instance.link is not None

        with tracer.start_span('serializing_data', child_of=request.span):
            data = AddressSerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update an Address record
        """
        return self.put(request, pk, True)


class VerboseAddressCollection(APIView):
    """
    Handles methods regarding Address records that do not require an id to be specified, i.e. list, create
    """

    serializer_class = AddressSerializer

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Address records

        description: |
            Retrieve a list of Address records that the requesting User is linked to.

        responses:
            200:
                description: A list of Address records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        # Create a list controller to parse user data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = AddressListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        kw = controller.cleaned_data['search']
        order = controller.cleaned_data['order']
        with tracer.start_span('get_objects', child_of=request.span) as span:
            try:
                with tracer.start_span('retrieve_requested_objects', child_of=span):
                    address_id = request.user.address['id']
                    # Get the list of Address objects
                    objs = Address.objects.prefetch_related(Prefetch(
                        'address_link',
                        AddressLink.objects.filter(address_id=address_id),
                        to_attr='link',
                    )).filter(
                        address_link__address_id=address_id,
                        **kw,
                    ).exclude(
                        **controller.cleaned_data['exclude'],
                    ).order_by(
                        *controller.cleaned_data['order'],
                    ).annotate(linked=Value(True, BooleanField()))
            except (ValueError, ValidationError):
                return Http400(error_code='membership_verbose_address_list_001')

        # Gather metadata
        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            warnings = controller.warnings
            # Get a string version of the order to return in the metadata
            meta_order = order[0] if len(order) == 1 else 'full_address' if '-' not in order[0] else '-full_address'
            metadata = {
                'page': page,
                'limit': limit,
                'order': meta_order,
                'total_records': total_records,
                'warnings': warnings,
            }
            # Pagination
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            # Cast all the prefetched lists of Address Links to AddressLink objects
            for o in objs:
                o.link = o.link[0]
            data = AddressSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})
