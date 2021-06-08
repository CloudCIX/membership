"""
Check receivers of Notifications in an Address for a specific Transaction
"""
# stdlib
from datetime import datetime
from typing import Optional
# libs
from cloudcix_rest.views import APIView
from cloudcix_rest.exceptions import Http404
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.request import Request
# local
from membership.controllers import UserListController
from membership.models import Address, Notification, TransactionType, User
from membership.permissions.notification import Permissions
from membership.serializers import UserSerializer

__all__ = [
    'NotificationCollection',
]


class NotificationCollection(APIView):
    """
    Handles methods regarding notification records that don't require an id to be specified
    """
    def get(self, request: Request, address_id: int, transaction_type_id: int) -> Response:
        """
        summary: Check what Users are to receive Notifications

        description: |
            Given an Address id and a Transaction Type id, retrieve a list of Users that are in the specified Address
            who will receive Notifications for Transactions of the specified Type.

            The list can also be filtered and ordered by the details of the Users.

        # Overwrite the default Controller
        controller: UserListController

        path_params:
            address_id:
                description: The id of the Address to find Users in
                type: integer
            transaction_type_id:
                description: The id of the Transaction Type to find Notifications for
                type: integer

        responses:
            200:
                description: A list of Users who are set up to receive the specified Notifications
                # The content doesn't follow the pattern (NotificationList) so we can overwrite it
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/UserList'
        """
        tracer = settings.TRACER

        # Check that address exists
        with tracer.start_span('retrieving_requested_address_object', child_of=request.span):
            try:
                address = Address.objects.get(pk=address_id)
            except Address.DoesNotExist:
                return Http404(error_code='membership_notification_list_001')

        # Check that transaction type exists
        with tracer.start_span('retrieving_requested_transaction_type_object', child_of=request.span):
            try:
                transaction_type = TransactionType.objects.get(pk=transaction_type_id)
            except TransactionType.DoesNotExist:
                return Http404(error_code='membership_notification_list_002')

        # Check the permissions
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.list(request, address)
            if err is not None:
                return err

        # Filter the notifications. Fetch users in the specified Address, and global active users in the Member
        address_filter = Q(user__address=address) | Q(user__global_active=True, user__member=address.member)
        with tracer.start_span('retrieving_notification_objects', child_of=request.span):
            notifications = Notification.objects.filter(
                address_filter,
                transaction_type=transaction_type,
            ).values_list(
                'user_id',
                flat=True,
            )

        # Get the controller
        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = UserListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_user_filters', child_of=span):
            user_filtering: Optional[Q] = None
            expired_user_filters = Q(
                pk__in=notifications,
                administrator=False,
                expiry_date__lt=datetime.utcnow().date(),
            )
            # If Member is self-managed only return Administrators or users who are public and not expired
            if address.member.self_managed:
                user_filtering = Q(
                    administrator=True,
                ) | Q(
                    expiry_date__gte=datetime.utcnow().date(),
                    is_private=False,
                )
                expired_user_filters &= Q(is_private=False)
            # If Member is not self-managed only return Administrators or users who have not expired.
            else:
                user_filtering = Q(
                    administrator=True,
                ) | Q(
                    expiry_date__gte=datetime.utcnow().date(),
                )

        with tracer.start_span('retrieving_user_objects', child_of=request.span):
            objs = User.objects.filter(
                pk__in=notifications,
                **controller.cleaned_data['search'],
            )
            if user_filtering is not None:
                objs = objs.filter(user_filtering)
            objs = objs.exclude(
                **controller.cleaned_data['exclude'],
            ).order_by(
                controller.cleaned_data['order'],
            )

            # Let the user know if there were Users who have expired
            expired_users = User.objects.filter(
                expired_user_filters,
                **controller.cleaned_data['search'],
            ).exclude(
                **controller.cleaned_data['exclude'],
            ).exists()

        with tracer.start_span('generating_metadata', child_of=request.span):
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            metadata = {
                'page': page,
                'limit': limit,
                'order': controller.cleaned_data['order'],
                'total_records': objs.count(),
                'expired_users': expired_users,
            }
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = UserSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})
