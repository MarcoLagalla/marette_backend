from django.core import validators as valids
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from backend.account.models import Business
from django_resized import ResizedImageField
from django.utils.text import slugify

from .declarations import FOOD_CATEGORY_CHOICES, FOOD_CATEGORY_CHOICES_IMAGES, DISCOUNT_TYPES_CHOICES


class Restaurant(models.Model):
    owner = models.ForeignKey(Business, related_name='restaurant', on_delete=models.CASCADE)
    slug = models.SlugField(unique=False, blank=True)
    url = models.SlugField(unique=True, blank=True)
    activity_name = models.CharField(max_length=30, unique=False, blank=False)
    activity_description = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    n_civ = models.IntegerField(blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    restaurant_number = PhoneNumberField(null=False, blank=False)
    p_iva = models.CharField(max_length=11, blank=False, unique=True)

    def __str__(self):
        return self.activity_name

    def set_url(self):
        self.slug = slugify(self.activity_name)
        self.url = str(self.id) + str('/') + slugify(self.activity_name)
        self.save()


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
    category = models.CharField(max_length=30, choices=FOOD_CATEGORY_CHOICES)
    image = models.ImageField(upload_to='product', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tags = models.ManyToManyField(ProductTag, blank=True)

    discounts = models.ManyToManyField(ProductDiscount, blank=True)
    show_image = models.BooleanField(blank=True, default=True)

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
        if not (self.image and hasattr(self.image, 'url')):
            try:
                return FOOD_CATEGORY_CHOICES_IMAGES.get(self.category)
            except KeyError:
                return FOOD_CATEGORY_CHOICES_IMAGES.get('Altro')
        else:
            return self.image.url


class MenuEntry(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    num_products = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    entries = models.ManyToManyField(MenuEntry, blank=True)

    def __str__(self):
        return self.name
