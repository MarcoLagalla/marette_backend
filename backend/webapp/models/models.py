import os
import random
import string
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core import validators as valids
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import serializers
from datetime import datetime

from backend.account.models import Business, Customer
from backend.webapp.declarations import FOOD_CATEGORY_CHOICES, FOOD_CATEGORY_CHOICES_IMAGES, \
    DISCOUNT_TYPES_CHOICES, FOOD_CATEGORY_CHOICES_THUMBS_IMAGES, RESTAURANT_CATEGORY_CHOICES, DAYS, DAILY_HOURS


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def gallery_component(instance, filename):
    name, extension = os.path.splitext(filename)
    extension = extension.lower()
    file_path = 'components/gallery/{rand}/{name}.{ext}'.format(
          rand=randomString(10), name=name, ext=extension)
    return file_path

def products_image(instance, filename):
    name, extension = os.path.splitext(filename)
    extension = extension.lower()
    file_path = 'products/{restaurant_id}/{rand}/{name}.{ext}'.format(
          restaurant_id=instance.restaurant.id, rand=randomString(5), name=name, ext=extension)
    return file_path

def products_image_thumb(instance, filename):
    name, extension = os.path.splitext(filename)
    extension = extension.lower()
    file_path = 'products/thumbnails/{restaurant_id}/{rand}/{name}.{ext}'.format(
          restaurant_id=instance.restaurant.id, rand=randomString(5), name=name, ext=extension)
    return file_path


class Restaurant(models.Model):
    owner = models.ForeignKey(Business, related_name='restaurant', on_delete=models.CASCADE)
    slug = models.SlugField(unique=False, default='', null=True, blank=True)
    url = models.CharField(max_length=150, unique=True, default='', null=True, blank=True)
    activity_name = models.CharField(max_length=30, unique=False, blank=False)
    activity_description = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    n_civ = models.CharField(max_length=10, blank=False)
    cap = models.PositiveIntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    restaurant_number = PhoneNumberField(null=False, blank=False)
    p_iva = models.CharField(max_length=11, blank=False)
    restaurant_category = models.ManyToManyField('Category', related_name='category_list', blank=False)

    restaurant_rank = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    customer_vote_list = models.ManyToManyField('CustomerVote', related_name='customer_vote_list', blank=True)

    image = ResizedImageField(size=[300, 300], crop=['middle', 'center'], quality=95, keep_meta=False,
                              upload_to='restaurant', blank=True, null=True, force_format='PNG')

    discounts = models.ManyToManyField('RestaurantDiscount', related_name='rest_discounts', blank=True)

    class Meta:
        unique_together = (('id', 'owner', 'p_iva'), )

    def __str__(self):
        return self.activity_name

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.set_url()
        super(Restaurant, self).save(*args, **kwargs)

    def set_url(self):
        self.slug = slugify(self.activity_name)
        self.url = str(self.id) + str('/') + slugify(self.activity_name)

    def set_restaurant_rank(self, rank):
        self.restaurant_rank = rank

    def discounts_count(self):
        return self.discounts.all().count()

    def get_image(self):
        if not (self.image and hasattr(self.image, 'url')):
            return settings.MEDIA_URL + 'placeholder/restaurant/rest_placeholder.png'
        else:
            return self.image.url

    def is_open(self, giorno=0):
        if giorno == 0:
            try:
                giorno = GiornoApertura.objects.all().filter(restaurant_id=self.id).get(day__iexact=str(today()))
                fasce = giorno.fasce
                if fasce:
                    for fascia in fasce.all():
                        this_hour = datetime.now().hour
                        if int(fascia.start[:2]) <= int(this_hour) <= int(fascia.end[:2]):
                            # aperto
                            return True
            except GiornoApertura.DoesNotExist as err:
                pass
            return False
        else:
            # voglio sapere se apre in qualsiasi momento in questo giorno
            try:
                giorno = GiornoApertura.objects.all().filter(restaurant_id=self.id).get(day__iexact=giorno)
                fasce = giorno.fasce
                if fasce.count() > 0:
                    return True
                else:
                    return False
            except GiornoApertura.DoesNotExist:
                pass
            return False

    def opens_at(self):
        if not self.is_open():
            try:
                giorno = GiornoApertura.objects.all().filter(restaurant_id=self.id).get(day__iexact=str(today()))
                fasce = giorno.fasce.all().order_by('start')
                if fasce:
                    for fascia in fasce:
                        this_hour = datetime.now().hour
                        if int(fascia.start[:2]) >= int(this_hour):
                            # apre a quest'ora
                            return "Apre alle " + fascia.start
            except GiornoApertura.DoesNotExist as err:
                    # oggi nessuna fascia di apertura
                    days_name = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']
                    days = ['1', '2', '3', '4', '5', '6', '7']
                    today_ = today()

                    before_ = days[:days.index(str(today_))]
                    next_ = days[days.index(str(today_)) + 1:]
                    next_days = next_ + before_

                    for day in next_days:
                        if self.is_open(day):
                            giorno = GiornoApertura.objects.all().filter(restaurant_id=self.id).get(
                                day__iexact=str(day))
                            fasce = giorno.fasce.all().order_by('start')
                            if fasce:
                                fascia = fasce.first()
                                return "Apre " + days_name[days.index(str(day))] + " alle " + fascia.start

                    return False
        else:
            return False


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True, blank=False)

    def __str__(self):
        return self.category_name


class CustomerVote(models.Model):
    vote = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)])
    customer = models.ForeignKey(Customer, related_name='customer_who_voted', on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey(Restaurant, related_name='restaurant_vote', on_delete=models.CASCADE)

    class Meta:
    #     unique_together = (('customer', 'restaurant'), )
        constraints = [
            models.UniqueConstraint(fields=['customer', 'restaurant'], name='unique_vote_for_user_at_rest')
        ]


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
        unique_together = (('restaurant', 'title', 'type', 'category', 'value'),)

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
        unique_together = (('restaurant', 'title', 'type', 'value'), )

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
        new_price = float(self.get_all_discounts())
        if new_price < 0:
            return "0.00"
        return "{:.2f}".format(new_price)

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
                return settings.MEDIA_URL + FOOD_CATEGORY_CHOICES_THUMBS_IMAGES.get(self.category)
            except KeyError:
                return settings.MEDIA_URL + FOOD_CATEGORY_CHOICES_THUMBS_IMAGES.get('Altro')
        else:
            return self.thumb_image.url

    def get_image(self):
        if not (self.image and hasattr(self.image, 'url')):
            try:
                return settings.MEDIA_URL + FOOD_CATEGORY_CHOICES_IMAGES.get(self.category)
            except KeyError:
                return settings.MEDIA_URL + FOOD_CATEGORY_CHOICES_IMAGES.get('Altro')
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
        return self.image.url


class FasciaOraria(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='fascia_oraria', on_delete=models.CASCADE)
    giorno = models.ForeignKey('GiornoApertura', related_name='giorno', on_delete=models.CASCADE)
    start = models.CharField(max_length=5, choices=DAILY_HOURS)
    end = models.CharField(max_length=5, choices=DAILY_HOURS)

    class Meta:
        unique_together = (('restaurant', 'giorno', 'start', 'end'), )

    def __str__(self):
        return "[{0}] {1} - {2}".format(self.restaurant, self.start, self.end)


class GiornoApertura(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='apertura_giorno', on_delete=models.CASCADE)
    orario = models.ForeignKey('OrarioApertura', related_name='orario', on_delete=models.CASCADE)
    day = models.CharField(max_length=9, choices=DAYS)
    fasce = models.ManyToManyField(FasciaOraria, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.restaurant, self.day)

    class Meta:
        unique_together = (('restaurant', 'day'), )


class OrarioApertura(models.Model):

    restaurant = models.ForeignKey(Restaurant, related_name='apertura', on_delete=models.CASCADE, unique=True)
    days = models.ManyToManyField(GiornoApertura, blank=True)

    def __str__(self):
        return "{0}".format(self.restaurant)



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


def today():
    date = datetime.today()
    day_name = ['Lunedi', 'Martedi', 'Mercoledi', 'Giovedi', 'Venerdi', 'Sabato', 'Domenica']
    day = datetime.strptime(date.strftime('%d %m %Y'), '%d %m %Y').weekday()
    return day + 1