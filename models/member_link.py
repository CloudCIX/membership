# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.urls import reverse
from django.db import models
# local
from .member import Member

__all__ = [
    'MemberLink',
    'MemberLinkManager',
]


class MemberLinkManager(BaseManager):
    """
    Manager for MemberLink which pre-fetches the related member objects
    """
    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always prefetches necessary data
        """
        return super().get_queryset().select_related(
            'member',
            'contra_member',
            'member__currency',
            'contra_member__currency',
        )


class MemberLink(BaseModel):
    """
    The MemberLink model tracks links between 2 Members in the DB.
    These Links are used to allow Members to interact with other Members.
    """
    contra_member = models.ForeignKey(Member, models.CASCADE, related_name='contra_member')
    member = models.ForeignKey(Member, models.CASCADE, related_name='member')

    objects = MemberLinkManager()

    class Meta:
        db_table = 'member_link'
        indexes = [
            models.Index(fields=['id'], name='member_link_id'),
            models.Index(fields=['deleted'], name='member_link_deleted'),
        ]

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the MemberLinkResource view for this MemberLink record
        :return: A URL that corresponds to the views for this MemberLink record
        """
        return reverse(
            'member_link_resource',
            kwargs={'member_id': self.member_id, 'contra_member_id': self.contra_member_id},
        )
