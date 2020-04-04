from django.urls import path
from .views import ListRestaurantsAPIView, CreateRestaurantAPIView

app_name = 'webapp'

urlpatterns = [
    path('restaurant/list', ListRestaurantsAPIView.as_view(), name='list_restaurant'),
    path('restaurant/new', CreateRestaurantAPIView.as_view(), name='register_restaurant'),
]
