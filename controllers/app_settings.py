# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from membership.models import AppSettings


__all__ = [
    'AppSettingsCreateController',
    'AppSettingsUpdateController',
]

SEGMENT_LENGTH = 63


class AppSettingsCreateController(ControllerBase):
    """
    Validates AppSettings data used to create a new AppSettings record
    """

    class Meta(ControllerBase.Meta):
        model = AppSettings
        validation_order = (
            'minio_access_key',
            'minio_secret_key',
            'minio_url',
        )

    def validate_minio_access_key(self, minio_access_key: Optional[str]) -> Optional[str]:
        """
        description: Access key is like user ID that uniquely identifies your MinIO account.
        required: false
        type: string
        """
        if minio_access_key is None:
            return None
        minio_access_key = str(minio_access_key).strip()

        if len(minio_access_key) > self.get_field('minio_access_key').max_length:
            return 'membership_app_settings_create_101'
        self.cleaned_data['minio_access_key'] = minio_access_key
        return None

    def validate_minio_secret_key(self, minio_secret_key: Optional[str]) -> Optional[str]:
        """
        description: Secret key is the password to your MinIO account.
        required: false
        type: string
        """
        if minio_secret_key is None:
            return None
        minio_secret_key = str(minio_secret_key).strip()
        if len(minio_secret_key) > self.get_field('minio_secret_key').max_length:
            return 'membership_app_settings_create_102'
        self.cleaned_data['minio_secret_key'] = minio_secret_key
        return None

    def validate_minio_url(self, minio_url: Optional[str]) -> Optional[str]:
        """
        description: The url for the MinIO instance for the COP.
        required: false
        type: string
        """
        if minio_url is None:
            return None
        minio_url = str(minio_url).strip()

        # Validate the domain minio_url for length and segment length
        if len(minio_url) > self.get_field('minio_secret_key').max_length:
            return 'membership_app_settings_create_103'

        # Ensure that each part of the minio_url, when split on '.', is not longer than 63 characters.
        if any(len(seg) > SEGMENT_LENGTH for seg in minio_url.split('.')):
            return 'membership_app_settings_create_104'

        self.cleaned_data['minio_url'] = minio_url
        return None


class AppSettingsUpdateController(ControllerBase):
    """
    Validates AppSettings data used to update an existing AppSettings
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields
        """
        model = AppSettings
        validation_order = (
            'minio_access_key',
            'minio_secret_key',
            'minio_url',
        )

    def validate_minio_access_key(self, minio_access_key: Optional[str]) -> Optional[str]:
        """
        description: Access key is like user ID that uniquely identifies your MinIO account.
        required: false
        type: string
        """
        if minio_access_key is None:
            return None
        minio_access_key = str(minio_access_key).strip()

        if len(minio_access_key) > self.get_field('minio_access_key').max_length:
            return 'membership_app_settings_update_101'
        self.cleaned_data['minio_access_key'] = minio_access_key
        return None

    def validate_minio_secret_key(self, minio_secret_key: Optional[str]) -> Optional[str]:
        """
        description: Secret key is the password to your MinIO account.
        required: false
        type: string
        """
        if minio_secret_key is None:
            return None
        minio_secret_key = str(minio_secret_key).strip()
        if len(minio_secret_key) > self.get_field('minio_secret_key').max_length:
            return 'membership_app_settings_update_102'
        self.cleaned_data['minio_secret_key'] = minio_secret_key
        return None

    def validate_minio_url(self, minio_url: Optional[str]) -> Optional[str]:
        """
        description: The url for the MinIO instance for the COP.
        required: false
        type: string
        """
        if minio_url is None:
            return None
        minio_url = str(minio_url).strip()

        # Validate the domain minio_url for length and segment length
        if len(minio_url) > self.get_field('minio_secret_key').max_length:
            return 'membership_app_settings_update_103'

        # Ensure that each part of the minio_url, when split on '.', is not longer than 63 characters.
        if any(len(seg) > SEGMENT_LENGTH for seg in minio_url.split('.')):
            return 'membership_app_settings_update_104'

        self.cleaned_data['minio_url'] = minio_url
        return None
