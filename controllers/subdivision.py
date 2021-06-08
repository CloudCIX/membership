from cloudcix_rest.controllers import ControllerBase


__all__ = [
    'SubdivisionListController',
]


class SubdivisionListController(ControllerBase):
    """
    Validates User data used to filter a list of Subdivision records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'english_name',
            'alpha_code',
            'id',
        )
        search_fields = {
            'alpha_code': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'english_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }
