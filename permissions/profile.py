# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import Profile, User


__all__ = [
    'Permissions',
]


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new Profile record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_profile_create_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_profile_create_202')

        return None

    @staticmethod
    def update(request: Request) -> Optional[Http403]:
        """
        The request to update a Profile record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_profile_update_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_profile_update_202')

        return None

    @staticmethod
    def delete(request: Request, obj: Profile) -> Optional[Http403]:
        """
        The request to delete a Profile record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        - The specified Profile is empty
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_profile_delete_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_profile_delete_202')

        # The specified Profile is empty
        if User.objects.filter(profile=obj).exists():
            return Http403(error_code='membership_profile_delete_203')

        return None
