"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/account/', include('backend.account.api.urls', 'account_api')),
    path('api/webapp/', include('backend.webapp.urls')),
    path('api/message/', include('backend.message.urls')),

]
