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
                'discount',
                'total',
                'iva',
                'items',
                'menus_items',
            )}),
    )
    readonly_fields = ('user', 'restaurant', 'date_created', 'code', 'discount', 'total', 'iva')

    # when in production
    # readonly_fields = ('user', 'restaurant', 'date_created', 'code', 'items', 'menus_items', 'total')

    def get_form(self, request, obj=None, **kwargs):
        # By passing 'fields', we prevent ModelAdmin.get_form from
        # looking up the fields itself by calling self.get_fieldsets()
        # If you do not do this you will get an error from
        # modelform_factory complaining about non-existent fields.

        kwargs['fields'] = flatten_fieldsets(self.fieldsets)
        return super(MyAdmin, self).get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(MyAdmin, self).get_fieldsets(request, obj)
        already = False
        for group, fields in fieldsets:
            if 'iva' in fields['fields'] or 'total' in fields['fields']\
                    or 'discount' in fields['fields']:
                already = True
        if not already:
            fieldsets[0][1]['fields'] += ('total', 'iva', 'discount',)

        return fieldsets

        return newfieldsets

    def total(self, obj):
        return obj.get_total()

    def iva(self, obj):
        return obj.get_total_iva()

    def discount(self, obj):
        return obj.get_total_discount()


admin.site.register(Order, MyAdmin)

admin.site.register(RestaurantDiscount)
