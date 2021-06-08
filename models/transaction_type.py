# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse
# local


__all__ = [
    'TransactionType',
]


class TransactionType(BaseModel):
    """
    The TransactionType model represents a transaction_type supported by CIX
    """
    # Fields
    name = models.TextField(null=True)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs

        db_table = 'transaction_type'
        indexes = [
            models.Index(fields=['id'], name='transaction_type_id'),
            models.Index(fields=['deleted'], name='transaction_type_deleted'),
            models.Index(fields=['name'], name='transaction_type_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the TransactionTypeResource view for this TransactionType record
        :return: A URL that corresponds to the views for this TransactionType record
        """
        return reverse('transaction_type_resource', kwargs={'pk': self.pk})
