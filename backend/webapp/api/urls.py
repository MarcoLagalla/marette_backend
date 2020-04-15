from django.urls import path
from .views import ListRestaurantsAPIView, CreateRestaurantAPIView, ShowRestaurantAPIView

app_name = 'webapp'

urlpatterns = [
    path('restaurant/list', ListRestaurantsAPIView.as_view(), name='list_restaurants'),
    path('restaurant/new', CreateRestaurantAPIView.as_view(), name='register_restaurant'),
    path('restaurant/<int:pk>/<slug:slug>', ShowRestaurantAPIView.as_view(), name='show_restaurant'),
]
