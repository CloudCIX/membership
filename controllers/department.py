# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from membership.models import Department

__all__ = [
    'DepartmentListController',
    'DepartmentCreateController',
    'DepartmentUpdateController',
]


class DepartmentListController(ControllerBase):
    """
    Validates User data used to list Department records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more
        specific for this Controller
        """
        allowed_ordering = (
            'name',
        )
        error_class = '010-114-005-004'
        search_fields = {
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class DepartmentCreateController(ControllerBase):
    """
    Validates User data used to create a new Department record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Department
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Department
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_department_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_department_create_102'
        department = Department.objects.filter(
            name=name,
            member_id=self.request.user.member['id'],
        )
        if department.exists():
            return 'membership_department_create_103'
        self.cleaned_data['name'] = name
        return None


class DepartmentUpdateController(ControllerBase):
    """
    Validates User data used to update a department record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Department
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Department
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_department_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_department_update_102'
        department = Department.objects.filter(
            name=name,
            member_id=self.request.user.member['id'],
        ).exclude(
            pk=self._instance.pk,
        )
        if department.exists():
            return 'membership_department_update_103'
        self.cleaned_data['name'] = name
        return None
