# libs
from django.db import models
from django.urls import reverse
# local
from .country import Country


__all__ = [
    'Subdivision',
]


class SubdivisionManager(models.Manager):

    def get_queryset(self) -> models.QuerySet:
        """
       Prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always prefetches necessary data
        """
        return super().get_queryset().select_related(
            'country',
        )


class Subdivision(models.Model):
    """
    The Subdivision model represents a part of a Country, like a state or county, etc.
    """
    alpha_code = models.CharField(max_length=5, null=True)
    country = models.ForeignKey(Country, models.CASCADE)
    english_name = models.CharField(max_length=50, null=True)

    # Use our custom manager
    objects = SubdivisionManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way is needed
        """
        db_table = 'subdivision'
        indexes = [
            models.Index(fields=['id'], name='subdivision_id'),
            models.Index(fields=['alpha_code'], name='subdivision_alpha_code'),
            models.Index(fields=['english_name'], name='subdivision_english_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the SubdivisionResource view for the Subdivision record
        :return: A URL that corresponds to views for the Subdivision record
        """
        return reverse('subdivision_resource', kwargs={'pk': self.pk, 'country_id': self.country.pk})
