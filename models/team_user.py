# libs
from django.db import models


__all__ = [
    'TeamUser',
]


class TeamUser(models.Model):
    """
    A table for handling the ManyToMany relationship between Team and User records
    """
    team = models.ForeignKey('Team', models.CASCADE)
    user = models.ForeignKey('User', models.CASCADE)

    class Meta:
        """
        Metadata about the model
        """
        db_table = 'team_user'
        unique_together = ('team', 'user')
