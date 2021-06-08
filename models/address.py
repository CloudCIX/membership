# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
# local
# import models directly since importing from membership.models breaks stuff
from .country import Country
from .currency import Currency
from .language import Language
from .member import Member
from .subdivision import Subdivision


__all__ = [
    'Address',
]


class AddressManager(BaseManager):
    """
    Manager for Address which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().select_related(
            'country',
            'currency',
            'language',
            'member',
            'member__currency',
            'subdivision',
            'subdivision__country',
        )


class Address(BaseModel):
    """
    An Address represents a physical location in which a Member has an office or is located in
    """
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, default='')
    address3 = models.CharField(max_length=100, default='')
    billing_address = models.ForeignKey('self', models.CASCADE, null=True)
    city = models.CharField(max_length=50)
    cloud_region = models.BooleanField(default=False)
    country = models.ForeignKey(Country, models.CASCADE)
    currency = models.ForeignKey(Currency, models.CASCADE, default=2)
    email = models.CharField(max_length=255, default='')
    gln = models.CharField(null=True, max_length=13)
    language = models.ForeignKey(Language, models.CASCADE, default=1)
    member = models.ForeignKey(Member, models.CASCADE)
    name = models.CharField(max_length=250)
    phones = JSONField(default=list)
    postcode = models.CharField(max_length=20, default='')
    subdivision = models.ForeignKey(Subdivision, models.CASCADE, null=True)
    vat_number = models.CharField(max_length=20, default='')
    website = models.CharField(max_length=50, default='')

    objects = AddressManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'address'
        indexes = [
            # Indexing everything in the `search_fields` map in List Controller
            models.Index(fields=['id'], name='address_id'),
            models.Index(fields=['address1'], name='address_address1'),
            models.Index(fields=['address2'], name='address_address2'),
            models.Index(fields=['address3'], name='address_address3'),
            models.Index(fields=['city'], name='address_city'),
            models.Index(fields=['cloud_region'], name='address_cloud_region'),
            models.Index(fields=['deleted'], name='address_deleted'),
            models.Index(fields=['name'], name='address_name'),
            models.Index(fields=['postcode'], name='address_postcode'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the AddressResource view for this Address record
        :return: A URL that corresponds to the views for this Address record
        """
        return reverse('address_resource', kwargs={'pk': self.pk})

    @property
    def full_address(self) -> str:
        """
        Generate the full address for the Address record. The full address is made up of:
            - company name
            - up to three address lines
            - city
            - subdivision
            - postcode
            - country name
        Ignoring any of these values that are null or empty
        :return: The full street address of the Address record
        """
        return ', '.join(filter(None, [
            self.name,
            self.address1,
            self.address2,
            self.address3,
            self.city,
            self.subdivision.english_name if self.subdivision is not None else None,
            self.postcode,
            self.country.english_name,
        ]))
