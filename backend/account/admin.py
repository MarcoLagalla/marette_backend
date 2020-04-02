from django.contrib import admin
from backend.account.models import Customer, Business
# Register your models here.

admin.site.register(Customer)
admin.site.register(Business)