from django.core import validators as valids
from django.db import models
from backend.account.models import BusinessUser


class Product(models.Model):
    product_id = models.PositiveIntegerField(default=0)
    activity = models.ForeignKey(BusinessUser, related_name='activity', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=600)
    #food_type = forms.ChoiceField(choices=FOOD_CATEGORY, widget=forms.RadioSelect())
    price = models.DecimalField(decimal_places=2, max_digits=5, validators=[valids.MinValueValidator(0.10)])
    vegetarian = models.BooleanField(default=False)