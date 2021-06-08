# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .member import Member


__all__ = [
    'Profile',
]


class ProfileManager(BaseManager):
    """
    Extend the base manager with select_related calls for this model
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


class Profile(BaseModel):
    """
    A Profile is another way of grouping Users in a Member, similar to Departments and Teams
    """
    member = models.ForeignKey(Member, models.CASCADE)
    name = models.CharField(max_length=50)

    objects = ProfileManager()

    class Meta:
        """
        Metadata about the model
        """
        db_table = 'profile'
        indexes = [
            models.Index(fields=['id'], name='profile_id'),
            models.Index(fields=['deleted'], name='profile_deleted'),
            models.Index(fields=['name'], name='profile_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the ProfileResource view for this Profile record
        :return: A URL that corresponds to the views for this Profile record
        """
        return reverse('profile_resource', kwargs={'pk': self.pk})
