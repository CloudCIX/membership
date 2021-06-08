"""
This file needs to be copied to framework/system_conf/urls_local.py
"""
from django.urls import include, path

urlpatterns = [
    path('', include('membership.urls')),
]
