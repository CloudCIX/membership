"""
Manage Users
"""
# stdlib
from datetime import datetime
from typing import Optional

# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from cloudcix_metrics import prepare_metrics, Metric
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import (
    UserCreateController,
    UserListController,
    UserUpdateController,
)
from membership.models import (
    AddressLink,
    Notification,
    User,
)
from membership.notifications import EmailConfirmationEmail as Email
from membership.permissions.user import Permissions
from membership.serializers import UserSerializer
from membership.utils import (
    ldap_add_memberuid,
    ldap_create,
    ldap_delete,
    ldap_exists,
    ldap_remove_memberuid,
    ldap_update_password,
)


__all__ = [
    'UserCollection',
    'UserResource',
]


class UserCollection(APIView):
    """
    Handles methods regarding User records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of User records

        description: |
            Retrieve a list of User records that the requesting User can read.

        responses:
            200:
                description: A list of User records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        # Validate the User parameters
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = UserListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_objects', child_of=request.span) as span:
            user_filtering: Optional[Q] = None
            search = controller.cleaned_data['search']
            try:
                with tracer.start_span('get_linked_address_ids', child_of=span):
                    if request.user.id != 1:
                        # If not, filter by linked Addresses instead
                        linked_address_ids = set(AddressLink.objects.filter(
                            address_id=request.user.address['id'],
                        ).values_list(
                            'contra_address_id',
                            flat=True,
                        ))
                        # Check if the User has already specified some ids to filter by
                        key = 'address_id__in'
                        if key in search:
                            set_ids = {int(i) for i in search[key]}
                            search[key] = set_ids & linked_address_ids
                        else:
                            search[key] = linked_address_ids

                        with tracer.start_span('get_active_public_users_for_partner_addresses', child_of=span):
                            # Return users who are;
                            # a) All Administrators
                            # b) All users in requesting users Member
                            # c) All users in non self-managed Partner Members
                            # c) Public users in self-managed Partner Members who have not expired
                            user_filtering = Q(
                                administrator=True,
                            ) | Q(
                                member_id=request.user.member['id'],
                            ) | Q(
                                member__self_managed=False,
                            ) | Q(
                                expiry_date__gte=datetime.utcnow().date(),
                                is_private=False,
                                member__self_managed=True,
                            )

                with tracer.start_span('retrieving_requested_objects', child_of=span):
                    # Get the list of User objects
                    order = controller.cleaned_data['order']

                    objs = User.objects.filter(
                        **search,
                    )

                    if user_filtering is not None:
                        objs = objs.filter(user_filtering)

                    objs = objs.exclude(
                        **controller.cleaned_data['exclude'],
                    ).order_by(
                        order,
                    )
            except (ValueError, ValidationError):
                return Http400(error_code='membership_user_list_001')

        # Gather metadata
        with tracer.start_span('generating_metadata', child_of=request.span):
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            warnings = controller.warnings
            total_records = objs.count()
            metadata = {
                'page': page,
                'limit': limit,
                'order': order,
                'total_records': total_records,
                'warnings': warnings,
            }
            # Pagination
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('checking_administrator', child_of=request.span):
            if not request.user.administrator:
                for obj in objs:
                    obj.first_otp = None
            else:
                for obj in objs:
                    if request.user.member != obj.member_id:
                        obj.first_otp = None

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = UserSerializer(instance=objs, many=True).data
        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new User record

        description: |
            Create a new User record using the data supplied by the User.

        responses:
            201:
                description: User record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        # Validate the sent data
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = UserCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)
        password = controller.cleaned_data.pop('password')

        # Check if the requesting user has permission to perform this request
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request, controller.instance.address)
            if err is not None:
                return err

        # Check if this is the first User in the Member
        with tracer.start_span('checking_if_first_user', child_of=request.span):
            if not User.objects.filter(member=controller.instance.member).exists():
                controller.instance.administrator = True

        # Modify the LDAP DB, either create the user outright, or update their existing entry to add another member id
        with tracer.start_span('modifying_LDAP', child_of=request.span):
            create_user = True
            # If we're testing, we might not need to create anything
            if settings.TESTING:
                conn = settings.LDAP_CONN
                create_user = not conn.search(
                    search_base=settings.LDAP_DOMAIN_CONTROLLER,
                    search_filter=f'(&(uid={controller.instance.email})(memberUid={controller.instance.member.id}))',
                )
            if create_user:
                if ldap_exists(controller.instance.email):
                    # LDAP entry exist for email so we will update it with the member_id
                    success = ldap_add_memberuid(controller.instance.email, controller.instance.member.id)
                else:
                    # Create new LDAP entry
                    success = ldap_create(controller.instance.email, controller.instance.member.id, password)
                if not success:  # pragma: no cover
                    return Http400(error_code='membership_user_create_001')

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        # Set up notifications for the User
        with tracer.start_span('adding_notifications_to_user', child_of=request.span):
            notifications = request.data.get('notifications', None)
            if ((request.user.member['id'] != controller.instance.member.pk or request.user.administrator) and
                    notifications is not None):
                # Loop through the sent details and get the transaction type id and whether its external or not
                Notification.objects.bulk_create(
                    Notification(
                        transaction_type_id=notification['transaction_type_id'],
                        user=controller.instance,
                        external=notification.get('external', True),
                    )
                    for notification in notifications
                )

        verify_email = False
        controller.instance.email_validated = True
        with tracer.start_span('email_verification', child_of=request.span):
            address = controller.instance.email.split('@')[1]
            if controller.instance.member.secret is False and address != 'nomail.com':
                # send email confirmation if not secret and not a nomail email
                controller.instance.email_validated = False
                verify_email = True

        # Post a metric for the creation of a User object
        prepare_metrics(lambda pk: Metric('user_create', pk, {}), pk=controller.instance.pk)

        # Generate user data
        with tracer.start_span('serializing_data', child_of=request.span):
            data = UserSerializer(instance=controller.instance).data

        if verify_email:
            with tracer.start_span('send_confirmation_email', child_of=request.span):
                email = Email()
                email.send(
                    request=self.request,
                    user=data,
                    to=controller.instance.email,
                    update=False,
                )
        # Return the response
        return Response({'content': data}, status=status.HTTP_201_CREATED)


class UserResource(APIView):
    """
    Handles methods regarding User records that do require an id to be specified, i.e. read, update,
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified User record

        description: |
            Attempt to read an User record by the given `pk`, returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the User record to be read
                type: integer

        responses:
            200:
                description: User record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Http404(error_code='membership_user_read_001')

        # Get the address link object to populate the User's Address serializer
        with tracer.start_span('retrieving_address_link_object', child_of=request.span):
            obj.address.link = None
            try:
                obj.address.link = AddressLink.objects.get(
                    address_id=request.user.address['id'],
                    contra_address=obj.address,
                )
            except AddressLink.DoesNotExist:
                pass

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        obj.address.linked = obj.address.link is not None

        with tracer.start_span('checking_administrator', child_of=request.span):
            if ((not request.user.administrator) or
               (request.user.administrator and request.user.member['id'] != obj.member_id)):
                obj.first_otp = None

        # Serialize the data and return it
        with tracer.start_span('serializing_data', child_of=request.span):
            data = UserSerializer(instance=obj).data
        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified User record

        description: |
            Attempt to update an User record by the given `pk`, returning a 404 if it does not exist.

        path_params:
            pk:
                description: The id of the User record to be updated
                type: integer

        responses:
            200:
                description: User record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        # Attempt to get the user information
        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Http404(error_code='membership_user_update_001')

        # Save some of the current user data
        current_address_id = obj.address.pk
        current_email = obj.email
        current_administrator = obj.administrator
        current_robot = obj.robot

        # Validate the user input
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = UserUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        # Retrieve the new password (if any)
        password = controller.cleaned_data.pop('password', None)

        # Check the permission for the update
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(
                request,
                obj,
                current_address_id,
                controller.instance.address_id,
                current_administrator,
                controller.instance.administrator,
                current_robot,
                controller.instance.robot,
            )
            if err is not None:
                return err

        update_password = False

        if password is not None:
            update_password = True

        email_changed = controller.instance.email != current_email
        if email_changed:
            # User's email needs to be changed in LDAP
            with tracer.start_span('modifying_LDAP', child_of=request.span) as span:

                add_memberuid = False
                create_new_ldap = False
                delete_current_ldap = False
                remove_memberuid = False

                if ldap_exists(current_email):
                    if User.objects.filter(email=current_email).exclude(pk=obj.pk).exists():
                        # If current email is in LDAP and in other members, remove member_id from LDAP entry.
                        remove_memberuid = True
                    else:
                        # If current email is not in other members, LDAP entry will be deleted.
                        delete_current_ldap = True

                if ldap_exists(controller.instance.email):
                    # If new email is in LDAP, add member_id to LDAP entry
                    add_memberuid = True
                else:
                    # New email is not in LDAP so a new LDAP entry will be created
                    create_new_ldap = True

                if create_new_ldap:
                    if not update_password:
                        return Http404(error_code='membership_user_update_002')
                    with tracer.start_span('create_ldap_entry', child_of=request.span) as span:
                        success = ldap_create(controller.instance.email, obj.member_id, password)
                    update_password = False

                    if not success:  # pragma: no cover
                        return Http400(error_code='membership_user_update_003')

                if add_memberuid:
                    with tracer.start_span('ldap_entry_add_memberuid', child_of=request.span) as span:
                        ldap_add_memberuid(controller.instance.email, obj.member_id)
                if remove_memberuid:
                    with tracer.start_span('ldap_entry_remove_memberuid', child_of=request.span) as span:
                        ldap_remove_memberuid(current_email, obj.member_id)
                if delete_current_ldap:
                    with tracer.start_span('delete_ldap_entry', child_of=request.span) as span:
                        ldap_delete(current_email)

        if update_password:
            if request.user.id == obj.pk or request.user.is_super:
                with tracer.start_span('updating_password', child_of=request.span) as span:
                    if ldap_exists(controller.instance.email):
                        # A user can only change their own password or a super user can
                        ldap_update_password(controller.instance.email, password)
                    else:
                        # Email for password, not in LDAP - create
                        ldap_create(controller.instance.email, obj.member_id, password)

        send_email_confirmation = request.data.get('send_email_confirmation', None)
        verify_email = False
        controller.instance.email_validated = obj.email_validated
        if send_email_confirmation or email_changed:
            with tracer.start_span('email_verification', child_of=request.span)as span:
                address = controller.instance.email.split('@')[1]
                # send email confirmation if not secret member and not a nomail.com email
                if controller.instance.member.secret is False and address != 'nomail.com':
                    controller.instance.email_validated = False
                    verify_email = True

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        # Set up notifications for the User
        with tracer.start_span('adding_notifications_to_user', child_of=request.span):
            notifications = request.data.get('notifications', None)
            if ((request.user.member['id'] != controller.instance.member.pk or request.user.administrator) and
                    notifications is not None):
                # Clear the old notifications for the user
                controller.instance.notifications.clear()
                # Loop through the sent details and get the transaction type id and whether its external or not
                Notification.objects.bulk_create(
                    Notification(
                        transaction_type_id=notification['transaction_type_id'],
                        user=controller.instance,
                        external=notification.get('external', True),
                    )
                    for notification in notifications
                )

        # Generate user data
        with tracer.start_span('serializing_data', child_of=request.span):
            data = UserSerializer(instance=controller.instance).data

        if verify_email:
            with tracer.start_span('send_confirmation_email', child_of=request.span):
                to = controller.instance.email
                update = False
                if request.user.id == obj.pk and email_changed:
                    # An email verification will be sent to the "current_email" if the user is updating
                    # their own email, otherwise an administrator is changing and it will be sent to the new
                    # email.
                    to = current_email
                    update = True
                email = Email()
                email.send(
                    request=self.request,
                    user=data,
                    to=to,
                    update=update,
                )

        # Generate and return the response
        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a User record
        """
        return self.put(request, pk, True)
