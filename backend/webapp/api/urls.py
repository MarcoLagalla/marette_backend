from django.urls import path

from .opening_hours_views import CreateOpening, CreateOpeningDay, CreateFasciaOraria, DeleteFasciaOraria, \
    DeleteOpeningDay, DeleteOpening, ShowTimeTable
from .views import ListRestaurantsAPIView, CreateRestaurantAPIView, ShowRestaurantAPIView, UpdateRestaurantAPIView, \
    VoteRestaurantAPIView, RestaurantCategoryAPIView, DeleteRestaurantAPIView
from .search_views import SearchRestaurantAPIView, SearchRestaurantByQueryAPIView, AutoComplete
from .products_views import AddProduct, ListProducts, DeleteProduct, UpdateProduct, ProductDetails, ListProductTags
from .discounts_views import *
from .menu_views import ListMenus, AddMenu, DetailsMenu, EditMenu, DeleteMenu, MenuEntryAdd, MenuEntryDetail, \
    MenuEntryEdit, MenuEntryDelete
from .components_views import *
from .orders_view import CreateOrder, OrderDetail

app_name = 'webapp'

urlpatterns = [

    path('restaurant/<int:id>/products', ListProducts.as_view(), name='list_products'),
    path('restaurant/<int:id>/products/add', AddProduct.as_view(), name='add_product'),
    path('restaurant/<int:id>/products/<int:p_id>/details', ProductDetails.as_view(), name='details_product'),
    path('restaurant/<int:id>/products/<int:p_id>/update', UpdateProduct.as_view(), name='update_product'),
    path('restaurant/<int:id>/products/<int:p_id>/delete', DeleteProduct.as_view(), name='delete_product'),

    path('restaurant/<int:id>/discounts', ListRestaurantDiscounts.as_view(), name='list_restaurant_discounts'),
    path('restaurant/<int:id>/discounts/add', AddRestaurantDiscounts.as_view(), name='add_restaurant_discounts'),
    path('restaurant/<int:id>/discounts/<int:d_id>/details', DetailsRestaurantDiscounts.as_view(), name='details_restaurant_discounts'),
    path('restaurant/<int:id>/discounts/<int:d_id>/edit', EditRestaurantDiscounts.as_view(), name='edit_restaurant_discounts'),
    path('restaurant/<int:id>/discounts/<int:d_id>/delete', DeleteRestaurantDiscounts.as_view(), name='delete_restaurant_discounts'),

    path('restaurant/<int:id>/products/discounts', ListDiscounts.as_view(), name='list_discounts'),
    path('restaurant/<int:id>/products/discounts/add', AddDiscounts.as_view(), name='add_discounts'),
    path('restaurant/<int:id>/products/discounts/<int:d_id>/details', DetailsDiscounts.as_view(), name='details_discounts'),
    path('restaurant/<int:id>/products/discounts/<int:d_id>/edit', EditDiscounts.as_view(), name='edit_discounts'),
    path('restaurant/<int:id>/products/discounts/<int:d_id>/delete', DeleteDiscounts.as_view(), name='delete_discounts'),
    path('restaurant/<int:id>/products/<int:p_id>/setdiscounts', SetDiscounts.as_view(), name='set_discounts'),


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

    path('restaurant/<int:id>/components/home/edit', UpdateHomeComponent.as_view(), name='edit_home_component'),
    path('restaurant/<int:id>/components/vetrina/edit', UpdateVetrinaComponent.as_view(), name='edit_vetrina_component'),
    path('restaurant/<int:id>/components/eventi/edit', UpdateEventiComponent.as_view(), name='edit_eventi_component'),
    path('restaurant/<int:id>/components/contattaci/edit', UpdateContattaciComponent.as_view(), name='edit_contattaci_component'),
    path('restaurant/<int:id>/components/menu/edit', UpdateMenuComponent.as_view(), name='edit_menu_component'),


    path('restaurant/<int:id>/components/galleria/images/add', GalleryAddImage.as_view(), name='add_picture_gallery'),
    path('restaurant/<int:id>/components/galleria/images/<int:i_id>/edit', GalleryEditImage.as_view(), name='edit_picture_gallery'),
    path('restaurant/<int:id>/components/galleria/images/<int:i_id>/delete', GalleryDeleteImage.as_view(), name='delete_picture_gallery'),

    # path('restaurant/<int:id>/opening/add', CreateOpening.as_view(), name='create_opening'),
    # path('restaurant/<int:id>/opening/delete', DeleteOpening.as_view(), name='delete_opening'),
    path('restaurant/<int:id>/opening/day/add', CreateOpeningDay.as_view(), name='create_opening_day'),
    path('restaurant/<int:id>/opening/day/<int:d_id>/delete', DeleteOpeningDay.as_view(), name='delete_opening_day'),
    path('restaurant/<int:id>/opening/day/<int:d_id>/interval/add', CreateFasciaOraria.as_view(), name='create_opening_interval'),
    path('restaurant/<int:id>/opening/day/<int:d_id>/interval/<int:f_id>/delete', DeleteFasciaOraria.as_view(), name='delete_opening_interval'),
    path('restaurant/<int:id>/timetable', ShowTimeTable.as_view(), name='show_timetable'),


    path('restaurant/list', ListRestaurantsAPIView.as_view(), name='list_restaurants'),
    path('restaurant/new', CreateRestaurantAPIView.as_view(), name='register_restaurant'),
    path('restaurant/search', SearchRestaurantAPIView.as_view(), name='search_restaurant'),
    path('restaurant/queryset', SearchRestaurantByQueryAPIView.as_view(), name='search_restaurant_query'),
    path('restaurant/category/list', RestaurantCategoryAPIView.as_view(), name='category_list'),
    path('restaurant/product/tags', ListProductTags.as_view(), name='list_product_tags'),
    path('restaurant/<int:id>', ShowRestaurantAPIView.as_view(), name='show_restaurant'),
    path('restaurant/<int:id>/update', UpdateRestaurantAPIView.as_view(), name='update_restaurant'),
    path('restaurant/<int:id>/delete', DeleteRestaurantAPIView.as_view(), name='delete_restaurant'),
    path('restaurant/<int:id>/vote', VoteRestaurantAPIView.as_view(), name='vote_restaurant'),

    path('restaurant/autocomplete', AutoComplete.as_view(), name='suggest_autocomplete'),

    path('order/new', CreateOrder.as_view(), name='create_order'),
    path('order/<int:id>/show', OrderDetail.as_view(), name='show_order'),
]
