"""
Dummy create controller to use for generating the AuthCreate schema
"""
# libs
from cloudcix_rest.controllers import ControllerBase


class AuthCreateController(ControllerBase):  # pragma: no cover
    """
    Authentication details for a User, plus optionally a Member's api_key
    """

    class Meta:
        # Validation Order is checked to generate schema
        validation_order = ('email', 'password', 'api_key')

    def validate_email(self):
        """
        description: The email for the User to be validated / authenticated
        type: string
        """
        return

    def validate_password(self):
        """
        description: The password for the User to authenticate with
        type: string
        """
        return

    def validate_api_key(self):
        """
        description: api_key of a Member to scope the token for the User
        type: string
        # Set this to be optional by specifying it is not required (default true)
        required: false
        """
        return
