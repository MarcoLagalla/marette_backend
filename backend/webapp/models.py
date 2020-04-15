from django.core import validators as valids
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from backend.account.models import Business
from django.utils.text import slugify


class Restaurant(models.Model):
    owner = models.ForeignKey(Business, related_name='restaurant', on_delete=models.CASCADE)
    url = models.SlugField(unique=True, blank=True)
    activity_name = models.CharField(max_length=30, unique=False, blank=False)
    activity_description = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    n_civ = models.IntegerField(blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    restaurant_number = PhoneNumberField(null=False, blank=False, help_text='Contact phone number')
    p_iva = models.CharField(max_length=11, blank=False, unique=True)
    # products =               # todo fai in seguito
    # menus =
    # etc ...

    def __str__(self):
        return self.activity_name

    def set_url(self):
        self.url = str(self.id) + str('/') + slugify(self.activity_name)
        self.save()



# class Product(models.Model):
#     product_id = models.PositiveIntegerField(default=0)
#     #activity = models.ForeignKey(BusinessUser, related_name='activity', on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#     description = models.TextField(max_length=600)
#     #food_type = forms.ChoiceField(choices=FOOD_CATEGORY, widget=forms.RadioSelect())
#     price = models.DecimalField(decimal_places=2, max_digits=5, validators=[valids.MinValueValidator(0.10)])
#     vegetarian = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
