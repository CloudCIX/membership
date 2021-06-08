# libs
from django.db import models
from django.urls import reverse


__all__ = [
    'Language',
]


class Language(models.Model):
    """
    The Language model represents a language that is supported by CloudCIX
    """
    code = models.CharField(max_length=6)
    english_name = models.CharField(max_length=25)
    native_name = models.CharField(max_length=50)  # name of language in itself

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'language'
        indexes = [
            models.Index(fields=['id'], name='language_id'),
            models.Index(fields=['code'], name='language_code'),
            models.Index(fields=['english_name'], name='language_english_name'),
            models.Index(fields=['native_name'], name='language_native_name'),
        ]

    def get_absolute_url(self) -> str:
        """
        Generates the absolute URL that corresponds to the LanguageResource view for this Language record
        :return: A URL that corresponds to the views for this Language record
        """
        return reverse('language_resource', kwargs={'pk': self.pk})
