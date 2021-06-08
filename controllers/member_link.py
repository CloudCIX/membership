# libs
from cloudcix_rest.controllers import ControllerBase


__all__ = [
    'MemberLinkListController',
]


class MemberLinkListController(ControllerBase):
    """
    Validates User data used to filter a list of MemberLink records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'id',
            'contra_member__name',
        )
        search_fields = {
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'member__id': ('in',),
            'member__self_managed': (),
            'contra_member__id': ('in',),
            'contra_member__self_managed': (),
        }
