from django.contrib import admin
from .models import Restaurant, Product, ProductTag, ProductDiscount, Menu, MenuEntry, RestaurantComponents, \
    HomeComponent, VetrinaComponent, EventiComponent, GalleriaComponent, MenuComponent, ContattaciComponent, Picture
# Register your models here.
admin.site.register(Restaurant)

admin.site.register(Product)
admin.site.register(ProductTag)
admin.site.register(ProductDiscount)

admin.site.register(Menu)
admin.site.register(MenuEntry)

admin.site.register(HomeComponent)
admin.site.register(VetrinaComponent)
admin.site.register(EventiComponent)
admin.site.register(GalleriaComponent)
admin.site.register(MenuComponent)
admin.site.register(ContattaciComponent)
admin.site.register(RestaurantComponents)


admin.site.register(Picture)