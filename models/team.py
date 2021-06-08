# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .member import Member
from .team_user import TeamUser
from .user import User


__all__ = [
    'Team',
]


class TeamManager(BaseManager):
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
        ).prefetch_related(
            'users',
            'users__address',
            'users__address__country',
            'users__address__currency',
            'users__address__language',
            'users__address__member',
            'users__address__member__currency',
            'users__address__subdivision',
            'users__address__subdivision__country',
            'users__department',
            'users__department__member',
            'users__department__member__currency',
            'users__language',
            'users__member',
            'users__member__currency',
            'users__profile',
            'users__profile__member',
            'users__profile__member__currency',
            'users__notifications',
        )


class Team(BaseModel):
    """
    The Team model represents a team within a Member
    """
    member = models.ForeignKey(Member, models.CASCADE)
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, through=TeamUser, related_name='teams')

    objects = BaseManager()
    # Prefetch only works for list when it's a ManyToMany field, so define two managers
    # One for list, and the BaseManager for single object views
    list_objects = TeamManager()

    class Meta:
        db_table = 'team'
        indexes = [
            models.Index(fields=['id'], name='team_id'),
            models.Index(fields=['deleted'], name='team_deleted'),
            models.Index(fields=['name'], name='team_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the MemberResource view for this Member record
        :return: A URL that corresponds to the views for this Member record
        """
        return reverse('team_resource', kwargs={'pk': self.pk})
