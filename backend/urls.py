"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # v1 API

    path('api/admin/', admin.site.urls),
    path('api/v1/account/', include('backend.account.api.urls', 'account_api')),
    path('api/v1/webapp/', include('backend.webapp.api.urls')),
]
