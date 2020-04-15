from django.contrib import admin
from .models import Restaurant, Product, ProductTag, ProductDiscount
# Register your models here.
admin.site.register(Restaurant)

admin.site.register(Product)
admin.site.register(ProductTag)
admin.site.register(ProductDiscount)