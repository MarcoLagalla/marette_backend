from django.core import validators as valids
from django.db import models
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from backend.account.models import Business
from django_resized import ResizedImageField


class Restaurant(models.Model):
    owner = models.ForeignKey(Business, related_name='restaurant', on_delete=models.CASCADE)
    url = models.SlugField(unique=True)
    activity_name = models.CharField(max_length=30, unique=False, blank=False)
    activity_description = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    restaurant_number = PhoneNumberField(null=False, blank=False, help_text='Contact phone number')
    p_iva = models.CharField(max_length=11, blank=False, unique=True)
    # products =               # todo fai in seguito
    # menus =
    # etc ...

    def __str__(self):
        return self.activity_name


FOOD_CATEGORY_CHOICES = [
    ('Altro', 'Altro'),
    ('Antipasto', 'Antipasto'),
    ('Primo', 'Primo'),
    ('Secondo', 'Secondo'),
    ('Contorno', 'Contorno'),
    ('Dessert', 'Dessert'),
    ('Caffetteria', 'Caffetteria'),
    ('Panetteria', 'Panetteria'),
    ('Panini e Piadine', 'Panini e Piadine'),
    ('Pizza', 'Pizza'),
    ('Primo', 'Primo'),
    ('Secondo', 'Secondo'),
    ('Snack', 'Snack'),
]

DISCOUNT_TYPES_CHOICES = [
    ('Fisso', 'Fisso'),
    ('Percentuale', 'Percentuale'),
]


class ProductTag(models.Model):
    name = models.CharField(max_length=100)
    icon = ResizedImageField(size=[32, 32], upload_to='tag_icon', null=True, blank=True, force_format='png')
    description = models.TextField()

    def __str__(self):
        return self.name


class ProductDiscount(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_discount', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=DISCOUNT_TYPES_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.type == 'Percentuale':
            if not self.value in range(0, 100):
                raise ValueError('Inserire un valore tra 0-100.')
        super(ProductDiscount, self).save(*args, **kwargs)


class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    image = models.ImageField(upload_to='product')
    category = models.CharField(max_length=30, choices=FOOD_CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField(ProductTag, blank=True)

    discounts = models.ManyToManyField(ProductDiscount, blank=True)

    def __str__(self):
        return self.name

    def get_all_discounts(self):
        price = self.price
        for discount in self.discounts.all():
            if discount.type == 'Fisso':
                # sconto fisso, da sottrarre al prezzo
                price -= discount.value
            elif discount.type == 'Percentuale':
                # sconto percentuale
                price -= round(price / 100 * discount.value, 2)
        return price

    def get_price_with_discount(self):
        new_price = self.get_all_discounts()
        if new_price < 0:
            new_price = 0
        return new_price

    def get_image(self):
        if self.image:
            return self.image.url


class Menu(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    products = models.ManyToManyField(Product, blank=True)  # menu di appartenenza

    def __str__(self):
        return self.name
