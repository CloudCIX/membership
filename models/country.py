# libs
from django.db import models
from django.urls import reverse
# local


__all__ = [
    'Country',
]


class Country(models.Model):
    """
    The Country model represents a country included in ISO 3166-1.
    """
    # Fields
    alpha_2_code = models.CharField(max_length=2)
    alpha_3_code = models.CharField(max_length=3)
    english_name = models.CharField(max_length=50)
    phone_prefix = models.IntegerField(null=True)
    primary_level_name = models.CharField(null=True, max_length=50)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'country'
        indexes = [
            models.Index(fields=['id'], name='country_id'),
            models.Index(fields=['alpha_2_code'], name='country_alpha_2_code'),
            models.Index(fields=['alpha_3_code'], name='country_alpha_3_code'),
            models.Index(fields=['english_name'], name='country_english_name'),
            models.Index(fields=['phone_prefix'], name='country_phone_prefix'),
            models.Index(fields=['primary_level_name'], name='country_primary_level_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the CountryResource view for this Country record
        :return: A URL that corresponds to the views for this Country record
        """
        return reverse('country_resource', kwargs={'pk': self.pk})
