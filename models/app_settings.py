# stdlib
# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse
# local

__all__ = [
    'AppSettings',
]


class AppSettings(BaseModel):
    """
    An App Settings object for optional minio settings
    """
    minio_access_key = models.CharField(max_length=100, null=True)
    minio_secret_key = models.CharField(max_length=100, null=True)
    minio_url = models.CharField(max_length=240, null=True)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'app_settings'

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the AppSettingsResource view for this AppSettings record
        :return: A URL that corresponds to the views for this AppSettings record
        """
        return reverse('app_settings_resource', kwargs={'pk': self.pk})
