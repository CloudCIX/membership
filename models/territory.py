# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.urls import reverse
from django.db import models
# local
from .member import Member

__all__ = [
    'Territory',
]


class TerritoryManager(BaseManager):
    """
    Manager for territory which pre-fetches the related member objects
    """
    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always prefetches necessary data
        """
        return super().get_queryset().select_related(
            'member',
            'member__currency',
        )


class Territory(BaseModel):
    member = models.ForeignKey(Member, models.CASCADE)
    name = models.CharField(max_length=50)

    objects = TerritoryManager()

    class Meta:
        db_table = 'territory'
        indexes = [
            models.Index(fields=['id'], name='territory_id'),
            models.Index(fields=['deleted'], name='territory_deleted'),
            models.Index(fields=['name'], name='territory_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the TerritoryResource view for this Territory record
        :return: A URL that corresponds to the views for this Territory record
        """
        return reverse('territory_resource', kwargs={'pk': self.pk})
