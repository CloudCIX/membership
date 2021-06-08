# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.urls import reverse
from django.db import models
# local
from .member import Member

__all__ = [
    'Department',
]


class DepartmentManager(BaseManager):
    """
    Manager for department which selects related member items
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


class Department(BaseModel):
    """
    A Department record describes a department within a company
    """
    member = models.ForeignKey(Member, models.CASCADE)
    name = models.CharField(max_length=50)

    objects = DepartmentManager()

    class Meta:
        db_table = 'department'
        indexes = [
            models.Index(fields=['id'], name='department_id'),
            models.Index(fields=['deleted'], name='department_deleted'),
            models.Index(fields=['name'], name='department_name'),
        ]

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the DepartmentResource view for this Department record
        :return: A URL that corresponds to the views for this Department record
        """
        return reverse('department_resource', kwargs={'pk': self.pk})
