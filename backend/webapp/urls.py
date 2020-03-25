from django.urls import path
import backend.webapp.views as webappviews

app_name = 'webapp'

urlpatterns = [
    #path('', webappviews.HomePageView.as_view(), name='homepage'),

   # path('<str:businessuser_name>/', webappviews.ShowActivityView.as_view(), name='activity-show'),
   # path('activity/new/', login_required(webappviews.NewActivityView.as_view()), name='activity-create'),   ###choice template, upload logo, img etc
   # path('activity/admin/', login_required(webappviews.AdminActivityView.as_view()), name='activity-admin'),
]
