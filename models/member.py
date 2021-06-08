# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .currency import Currency


__all__ = [
    'Member',
]


class MemberManager(BaseManager):
    """
    Extend the base manager with select_related calls for this model
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always prefetches necessary data
        """
        return super().get_queryset().select_related(
            'currency',
        )


class Member(BaseModel):
    """
    The Member model represents a company
    """
    api_key = models.CharField(max_length=64, blank=True)
    currency = models.ForeignKey(Currency, models.CASCADE)
    # global location number
    gln_prefix = models.CharField(null=True, max_length=12)
    name = models.CharField(max_length=250)
    secret = models.BooleanField(default=False)
    self_managed = models.BooleanField(default=False)

    objects = MemberManager()

    class Meta:
        db_table = 'member'
        indexes = [
            models.Index(fields=['api_key'], name='member_api_key'),
            models.Index(fields=['id'], name='member_id'),
            models.Index(fields=['deleted'], name='member_deleted'),
            models.Index(fields=['name'], name='member_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the MemberResource view for this Member record
        :return: A URL that corresponds to the views for this Member record
        """
        return reverse('member_resource', kwargs={'pk': self.pk})
