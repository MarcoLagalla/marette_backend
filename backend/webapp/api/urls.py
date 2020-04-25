from django.urls import path
from .views import ListRestaurantsAPIView, CreateRestaurantAPIView, ShowRestaurantAPIView, UpdateRestaurantAPIView
from .products_views import AddProduct, ListProducts, DeleteProduct, UpdateProduct, ProductDetails
from .discounts_views import ListDiscounts, AddDiscounts, EditDiscounts, DeleteDiscounts, DetailsDiscounts

app_name = 'webapp'

urlpatterns = [
    path('restaurant/list', ListRestaurantsAPIView.as_view(), name='list_restaurants'),
    path('restaurant/new', CreateRestaurantAPIView.as_view(), name='register_restaurant'),
    path('restaurant/<int:id>', ShowRestaurantAPIView.as_view(), name='show_restaurant'),
    path('restaurant/<int:id>/update', UpdateRestaurantAPIView.as_view(), name='update_restaurant'),

    path('restaurant/<int:id>/products', ListProducts.as_view(), name='list_products'),
    path('restaurant/<int:id>/products/add', AddProduct.as_view(), name='add_product'),
    path('restaurant/<int:id>/products/<int:p_id>/details', ProductDetails.as_view(), name='details_product'),
    path('restaurant/<int:id>/products/<int:p_id>/update', UpdateProduct.as_view(), name='update_product'),
    path('restaurant/<int:id>/products/<int:p_id>/delete', DeleteProduct.as_view(), name='delete_product'),

    path('restaurant/<int:id>/discounts', ListDiscounts.as_view(), name='list_discounts'),
    path('restaurant/<int:id>/discounts/add', AddDiscounts.as_view(), name='add_discounts'),
    path('restaurant/<int:id>/discounts/<int:d_id>/details', DetailsDiscounts.as_view(), name='details_discounts'),
    path('restaurant/<int:id>/discounts/<int:d_id>/edit', EditDiscounts.as_view(), name='edit_discounts'),
    path('restaurant/<int:id>/discounts/<int:d_id>/delete', DeleteDiscounts.as_view(), name='delete_discounts'),


]
