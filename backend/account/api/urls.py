from django.urls import path
from .views import CustomerAPIView, LoginGetToken, LogoutAPI, ListUsersAPIView, \
    BusinessAPIView, UpdatePassword

app_name = 'account'

urlpatterns = [
    path('customer', CustomerAPIView.as_view(), name='register_customer'),
    path('business', BusinessAPIView.as_view(), name='register_business'),
    path('login', LoginGetToken.as_view(), name='login'),
    path('logout', LogoutAPI.as_view(), name='logout'),
    path('list', ListUsersAPIView.as_view(), name='list'),
    path('password/<int:id>', UpdatePassword.as_view(), name='change_password'),
]