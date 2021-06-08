# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import Address, AddressLink


class Permissions:
    """
    Checks the permissions of the views.notification methods
    """

    @staticmethod
    def list(request: Request, address: Address) -> Optional[Http403]:
        """
        The request to list Notification records is valid if;
        - The specified Address is Linked to the requesting User's Address
        """
        # The specified Address is Linked to the requesting User's Address
        try:
            AddressLink.objects.get(
                address_id=request.user.address['id'],
                contra_address=address,
            )
        except AddressLink.DoesNotExist:
            return Http403(error_code='membership_notification_list_201')

        return None
