# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request


class Permissions:
    """
    Checks the permissions of the views.team methods
    """

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new Team record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_team_create_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_team_create_202')

        return None

    @staticmethod
    def update(request: Request) -> Optional[Http403]:
        """
        The request to update a Team record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_team_update_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_team_update_202')

        return None

    @staticmethod
    def delete(request: Request) -> Optional[Http403]:
        """
        The request to delete a Team record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_team_delete_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_team_delete_202')

        return None
