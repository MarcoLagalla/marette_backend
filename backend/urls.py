"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .api.views import index_view, MessageViewSet

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)

# urlpatterns = [
#
#     # http://localhost:8000/
#     path('', index_view, name='index'),
#
#     # http://localhost:8000/api/<router-viewsets>
#     path('api/', include(router.urls)),
#
#     # http://localhost:8000/api/admin/
#     path('api/admin/', admin.site.urls),
# ]



urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('user/', include('backend.account.urls')),
    path('', include('backend.webapp.urls')),
]

# debug (Marette -> settings.dev.py) must be set to False to show error page
handler403 = 'backend.webapp.views.error403'
handler404 = 'backend.webapp.views.error404'
