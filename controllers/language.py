# libs
from cloudcix_rest.controllers import ControllerBase


__all__ = [
    'LanguageListController',
]


class LanguageListController(ControllerBase):
    """
    Validates User data used to filter a list of Language records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller type
        """
        allowed_ordering = (
            'english_name',
            'code',
            'native_name',
        )
        search_fields = {
            'code': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'english_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'native_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }
