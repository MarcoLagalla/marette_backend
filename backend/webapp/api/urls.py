from django.urls import path
from .views import ListRestaurantsAPIView, CreateRestaurantAPIView, ShowRestaurantAPIView, UpdateRestaurantAPIView
from .products_views import AddProduct, ListProducts, DeleteProduct, UpdateProduct, ProductDetails, ListProductTags
from .discounts_views import ListDiscounts, AddDiscounts, EditDiscounts, DeleteDiscounts, DetailsDiscounts
from .menu_views import ListMenus, AddMenu, DetailsMenu, EditMenu, DeleteMenu, MenuEntryAdd, MenuEntryDetail, \
    MenuEntryEdit, MenuEntryDelete
from .components_views import ActivateComponent, DeactivateComponent
app_name = 'webapp'

urlpatterns = [

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

    path('restaurant/<int:id>/menus', ListMenus.as_view(), name='list_menus'),
    path('restaurant/<int:id>/menus/add', AddMenu.as_view(), name='add_menu'),
    path('restaurant/<int:id>/menus/<int:m_id>/details', DetailsMenu.as_view(), name='details_menu'),
    path('restaurant/<int:id>/menus/<int:m_id>/edit', EditMenu.as_view(), name='edit_menu'),
    path('restaurant/<int:id>/menus/<int:m_id>/delete', DeleteMenu.as_view(), name='delete_menu'),

    path('restaurant/<int:id>/menus/<int:m_id>/entry/add', MenuEntryAdd.as_view(), name='add_menuentry'),
    path('restaurant/<int:id>/menus/<int:m_id>/entry/<int:me_id>/details', MenuEntryDetail.as_view(), name='details_menuentry'),
    path('restaurant/<int:id>/menus/<int:m_id>/entry/<int:me_id>/edit', MenuEntryEdit.as_view(), name='edit_menuentry'),
    path('restaurant/<int:id>/menus/<int:m_id>/entry/<int:me_id>/delete', MenuEntryDelete.as_view(), name='delete_menuentry'),

    path('restaurant/<int:id>/components/<str:type>/activate', ActivateComponent.as_view(), name='on_component'),
    path('restaurant/<int:id>/components/<str:type>/deactivate', DeactivateComponent.as_view(), name='off_component'),

    path('restaurant/list', ListRestaurantsAPIView.as_view(), name='list_restaurants'),
    path('restaurant/new', CreateRestaurantAPIView.as_view(), name='register_restaurant'),
    path('restaurant/product/tags', ListProductTags.as_view(), name='list_product_tags'),
    path('restaurant/<int:id>', ShowRestaurantAPIView.as_view(), name='show_restaurant'),
    path('restaurant/<int:id>/update', UpdateRestaurantAPIView.as_view(), name='update_restaurant'),

]
