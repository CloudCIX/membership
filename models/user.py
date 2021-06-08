# stdlib
from typing import List
# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
# local
from .address import Address
from .department import Department
from .language import Language
from .member import Member
from .notification import Notification
from .profile import Profile
from .transaction_type import TransactionType


__all__ = [
    'User',
]


class UserManager(BaseManager):
    """
    Manager for User which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always prefetches necessary data
        """
        return super().get_queryset().select_related(
            'address',
            'address__country',
            'address__currency',
            'address__language',
            'address__member',
            'address__member__currency',
            'address__subdivision',
            'address__subdivision__country',
            'department',
            'department__member',
            'department__member__currency',
            'language',
            'member',
            'member__currency',
            'profile',
            'profile__member',
            'profile__member__currency',
        ).prefetch_related(
            'notifications',
            'teams',
        )


class User(BaseModel):
    """
    The User model represents a User in a company
    """
    address = models.ForeignKey(Address, models.CASCADE)
    administrator = models.BooleanField(default=False)
    department = models.ForeignKey(Department, models.CASCADE, null=True)
    email = models.CharField(max_length=255)
    expiry_date = models.DateTimeField()
    first_name = models.CharField(max_length=50)
    global_active = models.BooleanField(default=False)
    global_user = models.BooleanField(default=False)
    image = models.URLField(null=True)
    is_private = models.BooleanField(default=False)
    job_title = models.CharField(max_length=100, default='')
    language = models.ForeignKey(Language, models.CASCADE)
    last_login = models.DateTimeField(null=True)
    member = models.ForeignKey(Member, models.CASCADE)
    notifications = models.ManyToManyField(TransactionType, through=Notification, related_name='users')
    phones = JSONField(default=list)
    profile = models.ForeignKey(Profile, models.CASCADE, null=True)
    robot = models.BooleanField(default=False)
    signature = models.TextField(default='')
    start_date = models.DateTimeField()
    surname = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)
    otp = models.BooleanField(default=False)
    first_otp = models.IntegerField(null=True)
    email_validated = models.BooleanField(default=False)
    objects = UserManager()

    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['id'], name='user_id'),
            models.Index(fields=['administrator'], name='user_administrator'),
            models.Index(fields=['deleted'], name='user_deleted'),
            models.Index(fields=['email'], name='user_email'),
            models.Index(fields=['email_validated'], name='email_validated'),
            models.Index(fields=['expiry_date'], name='user_expiry_date'),
            models.Index(fields=['first_name'], name='user_first_name'),
            models.Index(fields=['global_active'], name='user_global_active'),
            models.Index(fields=['global_user'], name='user_global_user'),
            models.Index(fields=['is_private'], name='user_is_private'),
            models.Index(fields=['job_title'], name='user_job_title'),
            models.Index(fields=['last_login'], name='user_last_login'),
            models.Index(fields=['robot'], name='user_robot'),
            models.Index(fields=['start_date'], name='user_start_date'),
            models.Index(fields=['surname'], name='user_surname'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the UserResource view for this User record
        :return: A URL that corresponds to the views for this User record
        """
        return reverse('user_resource', kwargs={'pk': self.pk})

    def get_external_notifications(self) -> List[TransactionType]:
        """
        Returns a list of all the TransactionType records this User is set up to receive external notifications for
        :return: A list of TransactionType records
        """
        return TransactionType.objects.filter(notification__external=True, notification__user=self)

    def get_internal_notifications(self) -> List[TransactionType]:
        """
        Returns a list of all the TransactionType records this User is set up to receive internal notifications for
        :return: A list of TransactionType records
        """
        return TransactionType.objects.filter(notification__external=False, notification__user=self)
