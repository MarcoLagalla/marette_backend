from io import BytesIO

from PIL import Image
from django.core import validators as valids
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from backend.account.models import Business
from django_resized import ResizedImageField
from django.utils.text import slugify
import os
from .declarations import FOOD_CATEGORY_CHOICES, FOOD_CATEGORY_CHOICES_IMAGES, \
    DISCOUNT_TYPES_CHOICES, FOOD_CATEGORY_CHOICES_THUMBS_IMAGES

MAX_IMAGE_SIZE = 600000  # 600 KB for image


class Restaurant(models.Model):
    owner = models.ForeignKey(Business, related_name='restaurant', on_delete=models.CASCADE)
    slug = models.SlugField(unique=False, blank=True)
    url = models.SlugField(unique=True, blank=True)
    activity_name = models.CharField(max_length=30, unique=False, blank=False)
    activity_description = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    n_civ = models.PositiveIntegerField(blank=False)
    cap = models.PositiveIntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    restaurant_number = PhoneNumberField(null=False, blank=False)
    p_iva = models.CharField(max_length=11, blank=False, unique=True)

    def __str__(self):
        return self.activity_name

    def set_url(self):
        self.slug = slugify(self.activity_name)
        self.url = str(self.id) + str('/') + slugify(self.activity_name)
        self.save()


class HomeComponent(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='home', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[1920, 1080], quality=95, upload_to='components/home',
                              crop=['middle', 'center'], keep_meta=False, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_image(self):
        if not (self.image and hasattr(self.image, 'url')):
            return 'components/home/placeholder.png'
        else:
            return self.image.url

    def get_name(self):
        return self.name.upper()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)

            if len(img.fp.read()) > MAX_IMAGE_SIZE:
                compress_image(self.image.path, 70)

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name


def compress_image(img_file, CRATIO):
    img = Image.open(img_file)
    if len(img.fp.read()) > MAX_IMAGE_SIZE:
        img.save(img_file, format="JPEG", optimize=True, quality=CRATIO)
    img = Image.open(img_file)
    size = len(img.fp.read())
    return size


class VetrinaComponent(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='vetrina', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    menu_giorno = models.ForeignKey('Menu', related_name='menu_giorno', on_delete=models.DO_NOTHING,
                                    blank=True, null=True)
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_name(self):
        return self.name.upper()

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name


class MenuComponent(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_component', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_name(self):
        return self.name.upper()

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name


class GalleriaComponent(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='galleria_component', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    immagini = models.ManyToManyField('Picture', related_name='immagini', blank=True)
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_name(self):
        return self.name.upper()

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name


class EventiComponent(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='eventi_component', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_name(self):
        return self.name.upper()

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name


class ContattaciComponent(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='contattaci_component', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_name(self):
        return self.name.upper()

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name


class RestaurantComponents(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='components', on_delete=models.CASCADE)
    home = models.ForeignKey(HomeComponent, related_name='home_component', on_delete=models.DO_NOTHING, null=True, blank=True)
    vetrina = models.ForeignKey(VetrinaComponent, related_name='vetrina_component', on_delete=models.DO_NOTHING, null=True, blank=True)
    menu = models.ForeignKey(MenuComponent, related_name='menu_component', on_delete=models.DO_NOTHING, null=True, blank=True)
    galleria = models.ForeignKey(GalleriaComponent, related_name='galleria_component', on_delete=models.DO_NOTHING, null=True, blank=True)
    eventi = models.ForeignKey(EventiComponent, related_name='eventi_component', on_delete=models.DO_NOTHING, null=True, blank=True)
    contattaci = models.ForeignKey(ContattaciComponent, related_name='contattaci_component', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.restaurant.activity_name


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

    
    # TODO: dimensione massima foto prodotto
class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    category = models.CharField(max_length=30, choices=FOOD_CATEGORY_CHOICES)
    image = models.ImageField(upload_to='product', blank=True,null=True)
    thumb_image = models.ImageField(upload_to='product/thumbnails', blank=True, null=True)
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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    entries = models.ManyToManyField(MenuEntry, blank=True)

    def __str__(self):
        return self.name


class Picture(models.Model):

    image = ResizedImageField(size=[600, 600], upload_to='components/gallery', quality=95,
                              crop=['middle', 'center'], keep_meta=False)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name
