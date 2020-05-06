from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

from backend.account.models import Customer
from .models import Restaurant, Product
from .menu import Menu


ORDER_STATUS = [
    ('New', 'New'),
    ('Created', 'Created'),
    ('Confirmed', 'Confirmed'),
    ('Rejected', 'Rejected'),
    ('Payment Confirmed', 'Payment Confirmed'),
    ('Payment Declined', 'Payment Declined'),
]


class Order(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=255, choices=ORDER_STATUS)

    user = models.ForeignKey(Customer, related_name="carts", on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey(Restaurant, related_name="shop", on_delete=models.DO_NOTHING)

    items = models.ManyToManyField(Product, blank=True)
    menus_items = models.ManyToManyField(Menu, blank=True)

    code = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.restaurant.activity_name + "[{0}]".format(self.pk)

    def save(self, *args, **kwargs):
        self.code = generate_order_code(self.restaurant.id)
        super(Order, self).save(*args, **kwargs)

    def get_total(self):
        # for each items
        total = 0
        for item in self.items.all():
            total += item.get_price_with_discount()
        for menu in self.menus_items.all():
            total += menu.get_price()
        return "{:.2f}".format(total)

    def get_imposable(self):
        return float(self.get_total()) - float(self.get_total_iva())

    def get_total_iva(self):
        # for each items
        iva = 0
        for item in self.items.all():
            iva += item.get_iva()
        for menu in self.menus_items.all():
            iva += menu.get_iva()

        return "{:.2f}".format(iva)

    def get_total_discount(self):
        # for each items
        discount = 0
        for item in self.items.all():
            discount -= item.get_total_discount_amount()
        for menu in self.menus_items.all():
            pass
            # TODO: implementare discountMenu?
        return "{:.2f}".format(discount)

    def get_code(self):
        return self.code


def generate_order_code(id):
    digits = 10
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return str(id) + "-" + str(random.randint(lower, upper))
