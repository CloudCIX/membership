# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import AddressLink, Territory


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a Territory record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_territory_create_201')

        # The requesting User is an administrator
        if not request.user.administrator:
            return Http403(error_code='membership_territory_create_202')

        return None

    @staticmethod
    def update(request: Request) -> Optional[Http403]:
        """
        The request to update a Territory record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_territory_update_201')

        # The requesting User is an administrator
        if not request.user.administrator:
            return Http403(error_code='membership_territory_update_202')

        return None

    @staticmethod
    def delete(request: Request, obj: Territory) -> Optional[Http403]:
        """
        The request to delete a Territory record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator
        - The specified Territory record is not used in any Address Link
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_territory_delete_201')

        # The requesting User is an administrator
        if not request.user.administrator:
            return Http403(error_code='membership_territory_delete_202')

        # The specified Territory record is not used in any Address Link
        if AddressLink.objects.filter(territory=obj).exists():
            return Http403(error_code='membership_territory_delete_203')

        return None
