# stdlib
from typing import cast, Optional

# libs
from cloudcix_rest.controllers import ControllerBase

# local
from membership.models import Member, Currency

__all__ = [
    'MemberListController',
    'MemberCreateController',
    'MemberUpdateController',
]


class MemberListController(ControllerBase):
    """
    Validates User data used to filter a list of Member records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'id',
            'name',
        )
        error_class = '010-114-007-002'
        search_fields = {
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'api_key': ('in',),
        }


class MemberCreateController(ControllerBase):
    """
    Validates User data used to create a new Member record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Member
        validation_order = (
            'name',
            'currency_id',
            'gln_prefix',
            'secret',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Member
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_member_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_member_create_102'
        self.cleaned_data['name'] = name
        return None

    def validate_currency_id(self, currency_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the main Currency used by the Member
        type: integer
        """
        try:
            currency = Currency.objects.get(id=int(cast(int, currency_id)))
        except (TypeError, ValueError):
            return 'membership_member_create_103'
        except Currency.DoesNotExist:
            return 'membership_member_create_104'
        self.cleaned_data['currency'] = currency
        return None

    def validate_gln_prefix(self, gln_prefix: Optional[str]) -> Optional[str]:
        """
        description: The Global Location Number Prefix for the Member
        type: string
        required: false
        """
        if gln_prefix is None:
            gln_prefix = ''
        gln_prefix = str(gln_prefix).strip()
        if len(gln_prefix) > self.get_field('gln_prefix').max_length:
            return 'membership_member_create_105'
        self.cleaned_data['gln_prefix'] = gln_prefix
        return None

    def validate_secret(self, secret: Optional[bool]) -> Optional[str]:
        """
        description: |
            A flag stating whether the Member is a secret Member. A secret Member is only visible to the partner member
            that sent the  request
        type: boolean
        required: false
        """
        if secret is None:
            secret = False
        if not isinstance(secret, bool):
            return 'membership_member_create_106'
        self.cleaned_data['secret'] = secret
        return None


class MemberUpdateController(ControllerBase):
    """
    Validates User data used to update a Member record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Member
        validation_order = (
            'name',
            'currency_id',
            'gln_prefix',
            'self_managed',
            'secret',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Member
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_member_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_member_update_102'
        self.cleaned_data['name'] = name
        return None

    def validate_currency_id(self, currency_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the main Currency used by the Member
        type: integer
        """
        try:
            currency = Currency.objects.get(id=int(cast(int, currency_id)))
        except (TypeError, ValueError):
            return 'membership_member_update_103'
        except Currency.DoesNotExist:
            return 'membership_member_update_104'
        self.cleaned_data['currency'] = currency
        return None

    def validate_gln_prefix(self, gln_prefix: Optional[str]) -> Optional[str]:
        """
        description: The Global Location Number Prefix for the Member
        type: string
        required: false
        """
        if gln_prefix is None:
            gln_prefix = ''
        gln_prefix = str(gln_prefix).strip()
        if len(gln_prefix) > self.get_field('gln_prefix').max_length:
            return 'membership_member_update_105'
        self.cleaned_data['gln_prefix'] = gln_prefix
        return None

    def validate_self_managed(self, self_managed: Optional[bool]) -> Optional[str]:
        """
        description: Allow a User a non self-managed Member to make their Member self-managed
        type: boolean
        required: false
        """
        if self_managed is None:
            self_managed = self._instance.self_managed
        if not isinstance(self_managed, bool):
            return 'membership_member_update_106'
        # If the self_managed flag has remained the same, it's okay, so check that they're not trying to un-self-manage
        # a member
        if self._instance.self_managed and not self_managed:
            return 'membership_member_update_107'
        self.cleaned_data['self_managed'] = self_managed
        return None

    def validate_secret(self, secret: Optional[bool]) -> Optional[str]:
        """
        description: |
            A flag stating whether the Member is a secret Member. A secret Member is only visible to the partner member
            that sent the  request
        type: boolean
        required: false
        """
        if secret is None:
            secret = self._instance.secret
        if not isinstance(secret, bool):
            return 'membership_member_update_108'

        self_managed = self.cleaned_data.get('self_managed', self._instance.self_managed)

        if secret and self_managed:
            return 'membership_member_update_109'
        self.cleaned_data['secret'] = secret
        return None
