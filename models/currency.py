# libs
from django.urls import reverse
from django.db import models


__all__ = [
    'Currency',
]


class Currency(models.Model):
    """
    The Currency model represents a currency supported by CIX
    """
    name = models.CharField(max_length=25)
    symbol = models.CharField(max_length=5)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'currency'
        indexes = [
            models.Index(fields=['id'], name='currency_id'),
            models.Index(fields=['name'], name='currency_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the CurrencyResource view for this Currency record
        :return: A URL that corresponds to the views for this Currency record
        """
        return reverse('currency_resource', kwargs={'pk': self.pk})
