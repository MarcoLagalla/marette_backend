import random
import string

from PIL import Image
from django.db import models
from django_resized import ResizedImageField

from .models import Restaurant, Picture

MAX_IMAGE_SIZE = 600000  # 600 KB for image


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def home_component(instance, filename):
    name, ext = filename.split('.')
    file_path = 'components/home/{restaurant_id}/{rand}/{name}.{ext}'.format(
         restaurant_id=instance.restaurant.id, rand=randomString(5), name=name, ext=ext)
    return file_path


class HomeComponent(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='home', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[1920, 1080], quality=95, upload_to=home_component,
                              crop=['middle', 'center'], keep_meta=False, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_image(self):
        if not (self.image and hasattr(self.image, 'url')):
            return '/media/components/home/placeholder.png'
        else:
            return self.image.url

    def get_name(self):
        return self.name.upper()

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name


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
    show = models.BooleanField(default=False)

    class Meta:
        unique_together = ('restaurant', 'name',)

    def get_name(self):
        return self.name.upper()

    def __str__(self):
        return self.restaurant.__str__() + " : " + self.name

    def get_images(self):
        return Picture.objects.all().filter(restaurant=self.restaurant)


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


def compress_image(img_file, CRATIO):
    img = Image.open(img_file)
    if len(img.fp.read()) > MAX_IMAGE_SIZE:
        img.save(img_file, format="JPEG", optimize=True, quality=CRATIO)
    img = Image.open(img_file)
    size = len(img.fp.read())
    return size

