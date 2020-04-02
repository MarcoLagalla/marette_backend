from django.urls import path
from .views import CustomerAPIView

app_name = 'account'

urlpatterns = [
    path('', CustomerAPIView.as_view())
]