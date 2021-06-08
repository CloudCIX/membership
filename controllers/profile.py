# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from membership.models import Profile


class ProfileListController(ControllerBase):
    """
    Validates Profile data used to filter a list of Profile records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the Controller.Meta fields
        """
        allowed_ordering = (
            'name',
        )
        search_fields = {
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class ProfileCreateController(ControllerBase):
    """
    Validates Profile data used to create a new Profile record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Profile
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Profile
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_profile_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_profile_create_102'
        profile = Profile.objects.filter(name=name, member_id=self.request.user.member['id'])
        if profile.exists():
            return 'membership_profile_create_103'
        self.cleaned_data['name'] = name
        return None


class ProfileUpdateController(ControllerBase):
    """
    Validates Profile data used to update a Profile record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Profile
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Profile
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_profile_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_profile_update_102'
        profile = Profile.objects.filter(name=name, member=self._instance.member).exclude(pk=self._instance.pk)
        if profile.exists():
            return 'membership_profile_update_103'
        self.cleaned_data['name'] = name
        return None
