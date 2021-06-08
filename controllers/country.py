# libs
from cloudcix_rest.controllers import ControllerBase


__all__ = [
    'CountryListController',
]


class CountryListController(ControllerBase):
    """
    Validates User data used to filter a list of Country records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more
        specific for this Controller
        """
        # Allowed ordering should be in alphabetical order except for the
        # default ordering which should come first
        allowed_ordering = (
            'english_name',
            'alpha_2_code',
            'alpha_3_code',
            'phone_prefix',
            'primary_level_name',
        )
        error_class = '010-114-003-001'
        search_fields = {
            'alpha_2_code': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'alpha_3_code': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'english_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'phone_prefix': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'primary_level_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }
