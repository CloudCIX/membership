# stdlib
from typing import List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from membership.models import Team, User

__all__ = [
    'TeamCreateController',
    'TeamListController',
    'TeamUpdateController',
]


class TeamListController(ControllerBase):
    """
    Validates User data used to filter a list of Member records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more
        specific for this Controller
        """
        allowed_ordering = (
            'name',
        )
        search_fields = {
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class TeamCreateController(ControllerBase):
    """
    Validates User data used to create a new team record
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more
        specific for this Controller
        """
        model = Team
        validation_order = (
            'name',
            'users',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Team
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_team_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_team_create_102'
        self.cleaned_data['name'] = name
        return None

    def validate_users(self, users: Optional[List[int]]) -> Optional[str]:
        """
        description: An array of User ids representing Users from the Member to add to the Team once created
        type: array
        items:
            type: integer
        """
        if users is None:
            return None
        try:
            for user_id in users:
                if int(user_id) <= 0:
                    raise ValueError
        except (TypeError, ValueError):
            return 'membership_team_create_103'
        team_members = User.objects.filter(pk__in=users, member_id=self.request.user.member['id'])
        if len(users) != team_members.count():
            return 'membership_team_create_104'
        self.cleaned_data['users'] = team_members
        return None


class TeamUpdateController(ControllerBase):
    """
    Validates User data used to update a team record
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more
        specific for this Controller
        """
        model = Team
        validation_order = (
            'name',
            'users',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Team
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_team_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_team_update_102'
        self.cleaned_data['name'] = name
        return None

    def validate_users(self, users: Optional[List[int]]) -> Optional[str]:
        """
        description: |
            An array of User ids representing Users from the Member that should be in the Team.
            Removes all Users not in the array who are already in the Team.
        type: array
        items:
            type: integer
        """
        if users is None:
            return None
        try:
            for user_id in users:
                if int(user_id) <= 0:
                    raise ValueError
        except (TypeError, ValueError):
            return 'membership_team_update_103'
        team_members = User.objects.filter(pk__in=users, member_id=self.request.user.member['id'])
        if len(users) != team_members.count():
            return 'membership_team_update_104'
        self.cleaned_data['users'] = team_members
        return None
