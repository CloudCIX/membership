# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from membership.models import Territory

__all__ = [
    'TerritoryCreateController',
    'TerritoryListController',
    'TerritoryUpdateController',
]


class TerritoryListController(ControllerBase):
    """
    Validates User data used to filter a list of territory records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'name',
        )
        search_fields = {
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class TerritoryCreateController(ControllerBase):
    """
    Validates territory data used to create a new territory record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Territory
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Territory
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_territory_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_territory_create_102'
        # Check if territory exists
        if Territory.objects.filter(name=name, member=self.request.user.member['id']).exists():
            return 'membership_territory_create_103'
        self.cleaned_data['name'] = name
        return None


class TerritoryUpdateController(ControllerBase):
    """
    Validates User data used to update a territory record
    """

    class Meta(ControllerBase.Meta):
        """

        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Territory
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Territory
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_territory_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_territory_update_102'
        # Check if territory exists
        if Territory.objects.filter(name=name, member=self._instance.member).exists():
            return 'membership_territory_update_103'
        self.cleaned_data['name'] = name
        return None
