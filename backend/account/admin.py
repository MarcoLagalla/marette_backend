from django.contrib import admin
from backend.account.models import Customer, Business
# Register your models here.
from backend.account.tokens import account_activation_token
from backend.account.views import send_welcome_email


class CustomerAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super(CustomerAdmin, self).save_model(request, obj, form, change)
        customer = obj
        activation_token = account_activation_token.make_token(customer.user)
        send_welcome_email(customer.user, activation_token)
        super(CustomerAdmin, self).save_model(request, obj, form, change)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Business)