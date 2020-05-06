from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.forms import ModelForm
from rest_framework.exceptions import ValidationError

from .models.models import Restaurant, Product, ProductTag, ProductDiscount, Picture, RestaurantDiscount
from .models.menu import Menu, MenuEntry
from .models.components import RestaurantComponents, HomeComponent, VetrinaComponent, EventiComponent, \
    GalleriaComponent, MenuComponent, ContattaciComponent
from .models.orders import Order


class RestaurantAdmin(admin.ModelAdmin):
    readonly_fields = ('url', 'slug', )


admin.site.register(Restaurant, RestaurantAdmin)


class ProductInline(admin.ModelAdmin):
    model = Product
    exclude = ['thumb_image']


admin.site.register(Product, ProductInline)
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


class MyAdmin(ModelAdmin):

    fieldsets = (
        ('Order', {
            'fields': (
                'user',
                'restaurant',
                'date_created',
                'code',
                ('total', 'discount'),
                ('imposable', 'iva'),
                'items',
                'menus_items',
            )}),
    )
    readonly_fields = ('user', 'restaurant', 'date_created', 'code', 'discount', 'total', 'imposable', 'iva')

    # when in production
    # readonly_fields = ('all')

    def total(self, obj):
        return obj.get_total()

    def iva(self, obj):
        return obj.get_total_iva()

    def discount(self, obj):
        return obj.get_total_discount()

    def imposable(self, obj):
        return obj.get_imposable()

admin.site.register(Order, MyAdmin)

admin.site.register(RestaurantDiscount)
