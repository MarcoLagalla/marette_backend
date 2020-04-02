from django.urls import path
from .views import CustomerAPIView, LoginGetToken, LogoutAPI

app_name = 'account'

urlpatterns = [
    path('', CustomerAPIView.as_view()),
    path('login', LoginGetToken.as_view()),
    path('logout', LogoutAPI.as_view())
]