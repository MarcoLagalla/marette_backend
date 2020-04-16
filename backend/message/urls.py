from django.urls import path
from .views import MessageAPIView

app_name = 'message'

urlpatterns = [
    path('', MessageAPIView.as_view())
]
