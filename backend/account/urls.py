from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
import backend.account.views as webappviews
from backend.account.forms import LoginForm

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login_page.html', authentication_form=LoginForm),
         name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('signup/', webappviews.SignupView.as_view(), name='user-signup'),
    path('business-signup/', webappviews.BusinessSignupView.as_view(), name='business-signup'),
    path('<int:user_id>/', login_required(webappviews.UserProfileView.as_view()), name='user-profile'),
]
