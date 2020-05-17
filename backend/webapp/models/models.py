import random
import string
from io import BytesIO
from pathlib import Path

from PIL import Image
from django.conf import settings
from django.core import validators as valids
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers

from backend.account.models import Business
from django_resized import ResizedImageField
from django.utils.text import slugify
import os
from backend.webapp.declarations import FOOD_CATEGORY_CHOICES, FOOD_CATEGORY_CHOICES_IMAGES, \
    DISCOUNT_TYPES_CHOICES, FOOD_CATEGORY_CHOICES_THUMBS_IMAGES, RESTAURANT_CATEGORY_CHOICES


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def gallery_component(instance, filename):
    file_path = 'components/gallery/{rand}/{filename}'.format(
          rand=randomString(10), filename=filename)
    return file_path


def products_image(instance, filename):
    file_path = 'products/{restaurant_id}/{rand}/{filename}'.format(
          restaurant_id=instance.restaurant.id, rand=randomString(5), filename=filename)
    return file_path


def products_image_thumb(instance, filename):
    file_path = 'products/thumbnails/{restaurant_id}/{rand}/{filename}'.format(
          restaurant_id=instance.restaurant.id, rand=randomString(5), filename=filename)
    return file_path


class Restaurant(models.Model):
    owner = models.ForeignKey(Business, related_name='restaurant', on_delete=models.CASCADE)
    slug = models.SlugField(unique=False, default='', null=True, blank=True)
    url = models.CharField(max_length=150, unique=True, default='', null=True, blank=True)
    activity_name = models.CharField(max_length=30, unique=False, blank=False)
    activity_description = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    n_civ = models.PositiveIntegerField(blank=False)
    cap = models.PositiveIntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    restaurant_number = PhoneNumberField(null=False, blank=False)
    p_iva = models.CharField(max_length=11, blank=False)
    restaurant_category = models.CharField(max_length=100, choices=(RESTAURANT_CATEGORY_CHOICES + [('All', 'All'),]))

    image = ResizedImageField(size=[300, 300], crop=['middle', 'center'], quality=95, keep_meta=False,
                              upload_to='restaurant', blank=True, null=True, force_format='PNG')

    discounts = models.ManyToManyField('RestaurantDiscount', related_name='rest_discounts', blank=True)

    class Meta:
        unique_together = ('id', 'owner', 'p_iva')

    def __str__(self):
        return self.activity_name

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.set_url()
        super(Restaurant, self).save(*args, **kwargs)

    def set_url(self):
        self.slug = slugify(self.activity_name)
        self.url = str(self.id) + str('/') + slugify(self.activity_name)

    def discounts_count(self):
        return self.discounts.all().count()

    def get_image(self):
        if not (self.image and hasattr(self.image, 'url')):
            return '/media/placeholder/restaurant/placeholder.png'
        else:
            return self.image.url


class ProductTag(models.Model):
    name = models.CharField(max_length=100)
    icon = ResizedImageField(size=[32, 32], upload_to='tag_icon', null=True, blank=True, force_format='png')
    description = models.TextField()

    def __str__(self):
        return self.name


class RestaurantDiscount(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='activity_discount', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=DISCOUNT_TYPES_CHOICES)
    category = models.CharField(max_length=100, choices=(FOOD_CATEGORY_CHOICES + [('All', 'All'),]))
    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('restaurant', 'title', 'type', 'category', 'value')

    def __str__(self):
        return "[{0}] {1}".format(self.restaurant.url, self.title)

    def save(self, *args, **kwargs):
        if self.type == 'Percentuale':
            if not self.value in range(0, 100):
                raise serializers.ValidationError({'error': 'Inserire un valore tra 0-100.'})
        super(RestaurantDiscount, self).save(*args, **kwargs)


class ProductDiscount(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='product_discount', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=DISCOUNT_TYPES_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('restaurant', 'title', 'type', 'value')

    def __str__(self):
        return "[{0}] {1}".format(self.restaurant.url, self.title)

    def save(self, *args, **kwargs):
        if self.type == 'Percentuale':
            if not self.value in range(0, 100):
                raise serializers.ValidationError({'error': 'Inserire un valore tra 0-100.'})
        super(ProductDiscount, self).save(*args, **kwargs)


# TODO: dimensione massima foto prodotto
class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    category = models.CharField(max_length=30, choices=FOOD_CATEGORY_CHOICES)
    image = models.ImageField(upload_to=products_image, blank=True, null=True)
    thumb_image = models.ImageField(upload_to=products_image_thumb, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    iva = models.IntegerField(default=22, validators=[MinValueValidator(0), MaxValueValidator(100)])

    tags = models.ManyToManyField(ProductTag, blank=True)

    discounts = models.ManyToManyField(ProductDiscount, blank=True)
    show_image = models.BooleanField(blank=True, default=True)
    available = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return self.name

    def get_all_discounts(self):
        price = self.price
        # A restaurant-level discount override local product discount:
        if self.restaurant.discounts_count() > 0:
            for discount in self.restaurant.discounts.all():
                if discount.category == self.category or discount.category == 'All':
                    if discount.type == 'Fisso':
                        # sconto fisso, da sottrarre al prezzo
                        price -= discount.value
                    elif discount.type == 'Percentuale':
                        # sconto percentuale
                        price -= round(price / 100 * discount.value, 2)
            return price
        else:
            # no restaurant-level discount, see if product
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

    def get_original_price(self):
        return self.price

    def get_iva(self):
        return self.price - self.somma_imponibile()

    def somma_imponibile(self):
        return (100 * self.price) / (100 + self.iva)

    def get_total_discount_amount(self):
        discount = 0
        if self.restaurant.discounts_count() > 0:
            for d in self.restaurant.discounts.all():
                if d.category == self.category or d.category == 'All':
                    if d.type == 'Fisso':
                        # sconto fisso, da sottrarre al prezzo
                        discount -= d.value
                    elif d.type == 'Percentuale':
                        # sconto percentuale
                        discount -= round(self.price / 100 * d.value, 2)
            return discount
        else:
            for d in self.discounts.all():
                if d.type == 'Fisso':
                    # sconto fisso, da sottrarre al prezzo
                    discount -= d.value
                elif d.type == 'Percentuale':
                    # sconto percentuale
                    discount -= round(self.price / 100 * d.value, 2)
            return discount

    def get_thumb_image(self):
        if not (self.thumb_image and hasattr(self.thumb_image, 'url')):
            try:
                return FOOD_CATEGORY_CHOICES_THUMBS_IMAGES.get(self.category)
            except KeyError:
                return FOOD_CATEGORY_CHOICES_THUMBS_IMAGES.get('Altro')
        else:
            return self.thumb_image.url

    def get_image(self):
        if not (self.image and hasattr(self.image, 'url')):
            try:
                return FOOD_CATEGORY_CHOICES_IMAGES.get(self.category)
            except KeyError:
                return FOOD_CATEGORY_CHOICES_IMAGES.get('Altro')
        else:
            return self.image.url

    def save(self, *args, **kwargs):
        if not self.image.closed:
            if not self.make_thumb_image():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')
        super(Product, self).save(*args, **kwargs)

    def make_thumb_image(self):

        image = Image.open(self.image)
        image = image.resize(size=(150, 150))
        image.thumbnail((150, 150), Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumb_image.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


class Picture(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='gallery', on_delete=models.CASCADE)

    image = ResizedImageField(size=[600, 600], upload_to=gallery_component, quality=95,
                              crop=['middle', 'center'], keep_meta=False, force_format='PNG')
    name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name

    def get_image(self):
        print(self.image)
        return self.image.url


# to make thumb_image coherent with image cross DB modifications

@receiver(pre_save, sender=Product)
def do_something_if_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # Object is new, so field hasn't technically changed, but you may want to do something else here.
    else:
        if instance.image == '':
            instance.thumb_image = None
        if not obj.image == instance.image:  # Image has changed
            obj.thumb_image = None
            obj.save()