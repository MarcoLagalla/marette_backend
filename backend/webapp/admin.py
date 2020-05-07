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

    def save_model(self, request, obj, form, change):
        super(RestaurantAdmin, self).save_model(request, obj, form, change)
        obj.set_url()
        restaurant = obj
        # create ComponentsPanels (empty)
        home = HomeComponent.objects.create(restaurant=restaurant, name='HOME')
        vetrina = VetrinaComponent.objects.create(restaurant=restaurant, name='VETRINA')
        galleria = GalleriaComponent.objects.create(restaurant=restaurant, name='GALLERIA')
        eventi = EventiComponent.objects.create(restaurant=restaurant, name='EVENTI')
        menu = MenuComponent.objects.create(restaurant=restaurant, name='MENU')
        contattaci = ContattaciComponent.objects.create(restaurant=restaurant, name='CONTATTACI')

        RestaurantComponents.objects.create(
            restaurant=restaurant,
            home=home,
            vetrina=vetrina,
            galleria=galleria,
            eventi=eventi,
            menu=menu,
            contattaci=contattaci
        )

        super(RestaurantAdmin, self).save_model(request, obj, form, change)


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
