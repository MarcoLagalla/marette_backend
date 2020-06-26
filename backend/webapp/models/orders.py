from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.account.models import Customer
from .menu import Menu, MenuEntry
from .models import Restaurant, Product
from ...account.views import send_order_email


class OrderProductEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return "{} - {}".format(self.product, self.quantity)


class OrderMenuEntry(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return "{} - {}".format(self.menu, self.quantity)


class Order(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(Customer, related_name="carts", on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey(Restaurant, related_name="shop", on_delete=models.DO_NOTHING)

    items = models.ManyToManyField(OrderProductEntry, blank=True)
    menus_items = models.ManyToManyField(OrderMenuEntry, blank=True)

    def __str__(self):
        return self.restaurant.activity_name + "[{0}]".format(self.pk)

    def get_total(self):
        # for each items
        total = 0
        for item in self.items.all():
            total += (float(item.product.get_price_with_discount()) * item.quantity)
        for menu in self.menus_items.all():
            total += (float(menu.menu.get_price()) * menu.quantity)
        return "{:.2f}".format(total)

    def get_imposable(self):
        return float(self.get_total()) - float(self.get_total_iva())

    def get_total_iva(self):
        # for each items
        iva = 0
        for item in self.items.all():
            iva += (float(item.product.get_iva()) * item.quantity)
        for menu in self.menus_items.all():
            iva += (float(menu.menu.get_iva()) * menu.quantity)

        return "{:.2f}".format(iva)

    def get_total_discount(self):
        # for each items
        discount = 0
        for item in self.items.all():
            discount -= (float(item.product.get_total_discount_amount()) * item.quantity)
        return "{:.2f}".format(discount)

    def get_user(self):
        if not self.user:
            return 'Utente cancellato'
        return self.user

    def get_restaurant(self):
        if not self.restaurant:
            return 'Ristorante cancellato'
        return self.restaurant
