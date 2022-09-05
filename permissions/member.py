# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from membership.models import AddressLink, MemberLink, Member


class Permissions:

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a Member record is valid if;
        - The requesting User's Member is self-managed
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='membership_member_create_201')

        return None

    @staticmethod
    def read(request: Request, obj: Member) -> Optional[Http403]:
        """
        The request to read a Member record is valid if;
        - The specified Member is the requesting User's Member           TODO: Implement
        - The requesting User's Member is linked to the specified Member TODO: Remove
        """
        # Superuser User Allowance
        if request.user.id == 1:  # pragma: no cover
            return None

        # The requesting User's Member is linked to the specified Member - TODO: Remove
        try:
            MemberLink.objects.get(
                member_id=request.user.member['id'],
                contra_member=obj,
            )
        except MemberLink.DoesNotExist:
            return Http403(error_code='membership_member_read_201')

        return None

    @staticmethod
    def update(request: Request, obj: Member) -> Optional[Http403]:
        """
        The request to update a Member record is valid if;
        - The specified Member is self-managed and the requesting User is an administrator of that Member
        - The specified Member is non self-managed, the requesting User is an administrator of it and the request
            includes making the Member self-managed
        - The requesting User's Member is self-managed and the specified Member is a non self-managed partner
        """
        # Superuser User Allowance
        if request.user.id == 1:  # pragma: no cover
            return None

        # The specified Member is self-managed and the requesting User is an administrator of that Member
        if obj.self_managed and request.user.administrator and request.user.member['id'] == obj.id:
            return None

        # The specified Member is non self-managed, the requesting User is an administrator of it and the request
        # includes making the Member self-managed
        if (not obj.self_managed and request.data.get('self_managed', False) and request.user.member['id'] == obj.id and
                request.user.administrator):
            return None

        # The requesting User's Member is self-managed and the specified Member is a non self-managed partner
        if (AddressLink.objects.filter(address_id=request.user.address['id'], contra_address__member=obj).exists() and
                not obj.self_managed and request.user.member['self_managed']):
            # Partner without Member Link is if one of the other member's addresses are linked to the requesting user's
            return None

        # TODO - Turn this method around to return from the bad cases to allow for different error messages
        return Http403(error_code='membership_member_update_201')
