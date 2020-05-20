from django.urls import path
from .views import CustomerAPIView, LoginGetToken, LogoutAPI, ListUsersAPIView, \
    BusinessAPIView, UpdatePassword, ActivateUserAPIView, ResetPasswordAPIView, AskPasswordAPIView, \
    UserProfileAPIView, UpdateCostumerUserProfile, UpdateBusinessUserProfile, ResendActivationToken

app_name = 'account'

urlpatterns = [

    path('customer', CustomerAPIView.as_view(), name='register_customer'),
    path('business', BusinessAPIView.as_view(), name='register_business'),

    path('login', LoginGetToken.as_view(), name='login'),
    path('logout', LogoutAPI.as_view(), name='logout'),

    path('list', ListUsersAPIView.as_view(), name='list'),

    path('activate/resend/<int:id>', ResendActivationToken.as_view(), name='resend_token'),
    path('activate/<int:id>/<str:token>', ActivateUserAPIView.as_view(), name='activate_email'),

    path('password/<int:id>/change', UpdatePassword.as_view(), name='change_password'),
    path('password/reset', AskPasswordAPIView.as_view(), name='ask_reset_password'),
    path('password/reset/confirm', ResetPasswordAPIView.as_view(), name='reset_password'),

    path('profile/<int:id>', UserProfileAPIView.as_view(), name='profile'),
    path('profile/<int:id>/customer/update', UpdateCostumerUserProfile.as_view(), name='customer_update_profile'),
    path('profile/<int:id>/business/update', UpdateBusinessUserProfile.as_view(), name='business_update_profile'),
]