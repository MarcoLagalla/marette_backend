from django.urls import path
from .views import ListRestaurantsAPIView, CreateRestaurantAPIView, ShowRestaurantAPIView
from .products_views import AddProduct, ListProducts, DeleteProduct, UpdateProduct, ProductDetails
app_name = 'webapp'

urlpatterns = [
    path('restaurant/list', ListRestaurantsAPIView.as_view(), name='list_restaurants'),
    path('restaurant/new', CreateRestaurantAPIView.as_view(), name='register_restaurant'),
    path('restaurant/show/<slug:slug>', ShowRestaurantAPIView.as_view(), name='show_restaurant'),

    path('restaurant/<int:id>/products/', ListProducts.as_view(), name='list_products'),
    path('restaurant/<int:id>/products/add', AddProduct.as_view(), name='add_product'),
    path('restaurant/<int:id>/products/<int:p_id>/details', ProductDetails.as_view(), name='details_product'),
    path('restaurant/<int:id>/products/<int:p_id>/update', UpdateProduct.as_view(), name='update_product'),
    path('restaurant/<int:id>/products/<int:p_id>/delete', DeleteProduct.as_view(), name='delete_product'),

]
