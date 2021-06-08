# stdlib
from datetime import datetime
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import Address, AddressLink, User

__all__ = [
    'Permissions',
]


class Permissions:

    @staticmethod
    def create(request: Request, address: Address) -> Optional[Http403]:
        """
        The request to create a User record is valid if;
        - The requesting User's Member is self-managed
        - The specified Address is in the requesting User's Member or a non self-managed partner Member
        - The requestng User is an administrator
        """
        # Superuser User Allowance
        if request.user.is_super:  # pragma: no cover
            return None

        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_user_create_201')

        # The specified Address is in the requesting User's Member or a non self-managed partner Member
        if request.user.member['id'] != address.member_id and address.member.self_managed:
            return Http403(error_code='membership_user_create_202')

        # The requestng User is an administrator
        if not request.user.administrator:
            return Http403(error_code='membership_user_create_203')

        return None

    @staticmethod
    def read(request: Request, obj: User) -> Optional[Http403]:
        """
        The request to read a User record is valid if;
        - The requesting User's Address is linked to the specified User's Address in a non-self managed partner Member
        - The requesting User's Address is linked to the specified User's Address in self managed partner Member and
            the User is an Administrator or the User is not expired and the user.is_private is False.
        - The requesting User's Address is not linked to the specified User's Address but both are in the same Member
            and the requesting User is global
        """
        # The requesting User's Address is linked to the specified User's Address - This is tested in the view
        # The view only checks permissions if this is untrue

        # Superuser User Allowance
        if request.user.is_super:  # pragma: no cover
            return None

        # If the requesting User's Address is linked to the specified User's Address in a Partner Member and they are
        # non self managed or are self managed and the User is an Administrator or has a public active account.
        if obj.address.link and request.user.member['id'] != obj.member_id:
            if obj.member.self_managed:
                if obj.administrator:
                    return None
                if obj.expiry_date < datetime.utcnow():
                    return Http403(error_code='membership_user_read_201')
                if obj.is_private:
                    return Http403(error_code='membership_user_read_202')
            return None

        # If the Addresses are not linked, the specified User is in the requesting User's Member and the requesting User
        # is global
        if not obj.address.link:
            if request.user.member['id'] != obj.member_id:
                return Http403(error_code='membership_user_read_203')
            if not request.user.is_global:
                return Http403(error_code='membership_user_read_204')

        return None

    @staticmethod
    def update(
        request: Request,
        obj: User,
        current_address_id: int,
        new_address_id: int,
        current_administrator: bool,
        new_administrator: bool,
        current_robot: bool,
        new_robot: bool,
    ) -> Optional[Http403]:
        """
        The request to update a User record is valid if;
        - The requesting User's Member is self-managed
        - The specified User is in an Address linked to the request User's Address or the specified User is in the
            requesting User's Member and the requesting User is global
        - The specified User is in a non self-managed partner Member
        - The requesting User is updating themself, or is an administrator and updating some other User
        - The requesting User is a global User changing their Address or an administrator changing a User's Address
        """
        # Superuser User Allowance
        if request.user.is_super:  # pragma: no cover
            return None

        if current_administrator != new_administrator or current_robot != new_robot:
            return Http403(error_code='membership_user_update_201')

        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_user_update_202')

        # The specified User is in an Address linked to the request User's Address or the specified User is in the
        # requesting User's Member and the requesting User is global
        if request.user.member['id'] != obj.member_id or not request.user.is_global:
            # Check if an Address Link exists before raising a 403
            try:
                AddressLink.objects.get(
                    address_id=request.user.address['id'],
                    contra_address=obj.address,
                )
            except AddressLink.DoesNotExist:
                return Http403(error_code='membership_user_update_203')

        # The specified User is in a non self-managed partner Member
        if request.user.member['id'] != obj.member_id and obj.member.self_managed:
            return Http403(error_code='membership_user_update_204')
        else:
            # The requesting User is updating themself, or is an administrator and updating some other User
            if not request.user.administrator and not request.user.id == obj.pk:
                return Http403(error_code='membership_user_update_205')

        # The requesting User is a global User changing their Address or an administrator changing a User's Address
        if current_address_id != new_address_id:
            if not request.user.administrator and not obj.global_active:
                return Http403(error_code='membership_user_update_206')

        return None
