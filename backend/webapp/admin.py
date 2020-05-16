from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
import django.forms
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


class MenuInline(django.forms.ModelForm):

    entries = django.forms.MultipleChoiceField(disabled=True, required=False)

    class Meta:
        model = Menu
        fields = "__all__"
        readonly_fields = ('entries',)

    def __init__(self, *args, **kwargs):
        super(MenuInline, self).__init__(*args, **kwargs)
        choises = MenuEntry.objects.all().filter(menu=self.instance.pk).values_list('id', 'name')
        active_id = []
        for id, name in choises:
            active_id.append(id)
        self.fields['entries'] = django.forms.MultipleChoiceField(choices=choises)
        self.initial['entries'] = active_id
        self.fields['entries'].disabled = True
        self.fields['entries'].required = False

    def delete_model(self, request, obj):
        for entry in obj.entries.all():
            entry.delete()
        return super(MenuInline, self).delete_model(request, obj)


class MenuAdmin(ModelAdmin):
  form = MenuInline

admin.site.register(Menu, MenuAdmin)

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
                ('code', 'status'),
                ('total', 'discount'),
                ('imposable', 'iva'),
                'items',
                'menus_items',
                'valid',
            )}),
    )
    # readonly_fields = ('user', 'restaurant', 'date_created', 'code', 'discount', 'total', 'imposable', 'iva', )

    # when in production
    readonly_fields = ('discount', 'total', 'imposable', 'iva', 'date_created')

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
