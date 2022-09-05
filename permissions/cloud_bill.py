# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import Address


class Permissions:

    @staticmethod
    def read(request: Request, address: Address, target_address: Address) -> Optional[Http403]:
        """
        The request to read Cloudbill info is valid if;
        - The requesting user is from the target_address or the address's member (region or billing address)
        """
        # The requesting User is ID 1
        if request.user.id == 1:  # pragma: no cover
            return None

        # The requesting user is from the target_address or the address's member
        if request.user.address['id'] != target_address.pk and request.user.member['id'] != address.member_id:
            return Http403(error_code='membership_cloud_bill_read_201')

        return None
