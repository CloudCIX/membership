# libs
from django.db import models
# local


__all__ = [
    'Notification',
]


class Notification(models.Model):
    """
    A Notification record means that a User should receive notifications for a given transaction type
    """
    external = models.BooleanField(default=True)
    transaction_type = models.ForeignKey('TransactionType', models.CASCADE)
    user = models.ForeignKey('User', models.CASCADE)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'notifications'
        unique_together = ('transaction_type', 'user')
