# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models


class EmailConfirmation(models.Model):
    """
    The Email Confirmation model represent an email confirmation token
    """
    id = models.CharField(primary_key=True, max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.TextField()

    def get_user(self):
        """Returns a user with matching user_id

        :param int user_id: id of the user
        :returns: dict with user data or None
        :rtype: dict | None
        """
        data = json.loads(self.data)
        return data
