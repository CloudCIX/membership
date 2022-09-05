"""
Management of Members
"""

# stdlib
from hashlib import blake2b
from uuid import uuid4
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from cloudcix_metrics import prepare_metrics, Metric
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import (
    MemberCreateController,
    MemberListController,
    MemberUpdateController,
)
from membership.models import Member, MemberLink
from membership.permissions.member import Permissions
from membership.serializers import MemberSerializer

__all__ = [
    'MemberCollection',
    'MemberResource',
]


class MemberCollection(APIView):
    """
    Handles methods regarding Member records that do not require an id to be specified, i.e. list, create
    """
    # TODO: Remove list method as we are depracating MemberLink entirely
    #       - Ensure all other applications and apps do not use member.list
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Member records

        description: |
            Retrieve a list of Member records that the requesting User's Member is linked to.

        deprecated: true

        responses:
            200:
                description: A list of Member records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MemberListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_objects', child_of=request.span) as span:
            kw = controller.cleaned_data['search']
            order = controller.cleaned_data['order']
            try:
                # Get the members that are linked to the User's for listing
                with tracer.start_span('get_linked_member_ids', child_of=span):
                    linked_members = set(MemberLink.objects.filter(
                        member_id=request.user.member['id'],
                    ).values_list(
                        'contra_member_id',
                        flat=True,
                    ))
                    if kw.get('id__in', False):
                        id_set = {int(i) for i in kw['id__in']}
                        kw['id__in'] = id_set & linked_members
                    else:
                        kw['id__in'] = linked_members
                with tracer.start_span('retrieve_requested_objects', child_of=span):
                    # Get the list of Member objects
                    objs = Member.objects.filter(
                        **kw,
                    ).exclude(
                        **controller.cleaned_data['exclude'],
                    ).order_by(
                        order,
                    )
            except(ValueError, ValidationError):
                return Http400(error_code='membership_member_list_001')

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
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = MemberSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Member record

        description: |
            Create a new Member record using the data supplied by the User.

        responses:
            201:
                description: Member record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        # Start by checking the permissions
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        # Validate the User data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MemberCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        # Save the new Member and set up the needed Member Links
        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        # TODO: Remove when Member Link has been removed from all other applications and apps
        # Link the Member to itself
        with tracer.start_span('creating_self_link', child_of=request.span):
            self_link = MemberLink.objects.create(member=controller.instance, contra_member=controller.instance)
            self_link.save()

        # Create the links between the new member and the user's member
        with tracer.start_span('creating_user_member_links', child_of=request.span):
            user_member = Member.objects.get(id=request.user.member['id'])
            link1 = MemberLink.objects.create(member=user_member, contra_member=controller.instance)
            link1.save()
            link2 = MemberLink.objects.create(member=controller.instance, contra_member=user_member)
            link2.save()

        with tracer.start_span('generating_api_key', child_of=request.span):
            controller.instance.refresh_from_db()
            # The os_id has been replaced with api key which is a 64 character string that is entirely random
            api_key = blake2b(uuid4().bytes, digest_size=32).hexdigest()
            while Member.objects.filter(api_key=api_key).exists():  # pragma: no cover
                # Prevent an overlap of api_keys
                api_key = blake2b(uuid4().bytes, digest_size=32).hexdigest()
            controller.instance.api_key = api_key
            controller.instance.save()

        # Send a metric to indicate a Member record has been created
        prepare_metrics(lambda pk: Metric('member_create', pk, {}), pk=controller.instance.pk)

        with tracer.start_span('serializing_data', child_of=request.span):
            data = MemberSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class MemberResource(APIView):
    """
    Handles methods regarding Member records that do require an id to be specified, i.e. read, update, delete
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Member record

        description: |
            Attempt to read a Member record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Member record to be read
                type: integer

        responses:
            200:
                description: Member record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Member.objects.get(id=pk)
            except Member.DoesNotExist:
                return Http404(error_code='membership_member_read_001')

        # Check that the user has permission to read this object
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        # Serialize the object and return it
        with tracer.start_span('serializing_data', child_of=request.span):
            data = MemberSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Member record

        description: |
            Attempt to update a Member record by the given `pk`, returning a 404 if it does not exist.

        path_params:
            pk:
                description: The id of the Member record to be updated
                type: integer

        responses:
            200:
                description: Member record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Member.objects.get(id=pk)
            except Member.DoesNotExist:
                return Http404(error_code='membership_member_update_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request, obj)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MemberUpdateController(
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
            data = MemberSerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Member record
        """
        return self.put(request, pk, True)
