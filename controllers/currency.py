# libs
from cloudcix_rest.controllers import ControllerBase


__all__ = [
    'CurrencyListController',
]


class CurrencyListController(ControllerBase):
    """
    Validates User data used to filter a list of Currency records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more
        specific for this Controller
        """
        # Allowed ordering should be in alphabetical order except for the
        # default ordering which should come first
        allowed_ordering = (
            'name',
        )
        search_fields = {
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }
