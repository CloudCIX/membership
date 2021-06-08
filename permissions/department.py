# stdlib
from typing import Optional
# lib
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import Department, User


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a new Department record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_department_create_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_department_create_202')

        return None

    @staticmethod
    def update(request: Request) -> Optional[Http403]:
        """
        The request to update a Department record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_department_update_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_department_update_202')

        return None

    @staticmethod
    def delete(request: Request, obj: Department) -> Optional[Http403]:
        """
        The request to delete a Department record is valid if;
        - The requesting User's Member is self-managed
        - The requesting User is an administrator of their Member
        - The specified Department is empty
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_department_delete_201')

        # The requesting User is an administrator of their Member
        if not request.user.administrator:
            return Http403(error_code='membership_department_delete_202')

        # The specified Department is empty
        if User.objects.filter(department=obj).exists():
            return Http403(error_code='membership_department_delete_203')

        return None
