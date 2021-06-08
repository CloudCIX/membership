# libs
from django.db import models


__all__ = [
    'IntegrityTest',
]


class IntegrityTest(models.Model):
    errors_found = models.IntegerField()
    finish_time = models.DateTimeField()
    records_inspected = models.IntegerField()
    start_time = models.DateTimeField()
