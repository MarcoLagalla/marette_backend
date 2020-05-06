from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Restaurant, Product


class MenuEntry(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    num_products = models.PositiveIntegerField(default=1, validators=[MinValueValidator(0)])
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    iva = models.IntegerField(default=22, validators=[MinValueValidator(0), MaxValueValidator(100)])

    entries = models.ManyToManyField(MenuEntry, blank=True)

    def __str__(self):
        return self.name

    def get_price(self):
        return self.price

    def get_iva(self):
        return self.get_price() - self.somma_imponibile()

    def somma_imponibile(self):
        return (100 * self.get_price()) / (100 + self.iva)