from django.db import models
from django.core.validators import MinValueValidator

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

    items = models.ManyToManyField(Product)
    menus_items = models.ManyToManyField(Menu)

    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.restaurant.activity_name + "[{0}]".format(self.pk)

    def get_total(self):
        # for each items
        total = 0
        for item in self.items:
            total += item.get_price_with_discount()
        for menu in self.menus_items:
            total += menu.get_price()
        return total

    def get_total_discount(self):
        # for each items
        discount = 0
        for item in self.items:
            discount -= item.get_total_discount_amount()
        for menu in self.menus_items:
            # TODO: implementare discountMenu
        return discount
