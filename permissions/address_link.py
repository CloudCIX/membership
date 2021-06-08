# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import Address, AddressLink


class Permissions:

    @staticmethod
    def create(request: Request, contra_address: Address) -> Optional[Http403]:
        """
        The request to create an Address Link record is valid if;
        - The requesting User's Member is self managed
        - An Address Link does not already exist between the requesting User's Address and the specified Address
        """
        # The requesting User's Member is self managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_address_link_create_201')

        # An Address Link does not already exist between the requesting User's Address and the specified Address
        try:
            AddressLink.objects.get(
                address_id=request.user.address['id'],
                contra_address=contra_address,
            )
            return Http403(error_code='membership_address_link_create_202')
        except AddressLink.DoesNotExist:
            pass

        return None

    @staticmethod
    def update(request: Request) -> Optional[Http403]:
        """
        The request to create an Address Link record is valid if;
        - The requesting User's Member is self-managed
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_address_link_update_201')

        return None
