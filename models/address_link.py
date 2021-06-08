# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .address import Address
from .territory import Territory

__all__ = [
    'AddressLink',
]


class AddressLinkManager(BaseManager):
    """
    Manager for address link which selects addresses related to the AddressLink
    """
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related(
            'address',
            'address__country',
            'address__currency',
            'address__language',
            'address__member',
            'address__member__currency',
            'address__subdivision',
            'address__subdivision__country',
            'contra_address',
            'contra_address__country',
            'contra_address__currency',
            'contra_address__language',
            'contra_address__member',
            'contra_address__member__currency',
            'contra_address__subdivision',
            'contra_address__subdivision__country',
        )


class AddressLink(BaseModel):
    """
    The AddressLink model represents a link between two address records, indicating they do business, etc
    """
    address = models.ForeignKey(Address, models.CASCADE, related_name='address_contra_link')
    client = models.BooleanField(default=False)
    compute = models.BooleanField(default=False)
    contra_address = models.ForeignKey(Address, models.CASCADE, related_name='address_link')
    credit_limit = models.DecimalField(null=True, max_digits=23, decimal_places=4)
    customer = models.BooleanField(default=False)
    note = models.TextField(null=True)
    reference = models.CharField(max_length=20, default='')
    service_centre = models.BooleanField(default=False)
    supplier = models.BooleanField(default=False)
    territory = models.ForeignKey(Territory, models.CASCADE, null=True)
    warrantor = models.BooleanField(default=False)

    objects = AddressLinkManager()

    class Meta:
        db_table = 'address_link'

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the AddressLinkRescource view for this AddressLink record
        :return: A URL that corresponds to the views for this AddressLink record
        """
        return reverse('address_link_resource', kwargs={'address_id': self.contra_address.pk})
