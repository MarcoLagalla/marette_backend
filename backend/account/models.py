import random
import string
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core import validators as valids
from django.db import models
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def content_file_name(instance, filename):
    ext = Path(filename).suffix
    file_path = 'avatars/{customer_id}/{rand}/avatar{ext}'.format(
         customer_id=instance.user.id, rand=randomString(5), ext=ext)
    return file_path


class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

    avatar = ResizedImageField(size=[250, 250], quality=95, crop=['middle', 'center'],
                               keep_meta=False, upload_to=content_file_name, blank=True, null=True)

    birth_date = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(unique=True, error_messages={'unique': 'Esiste già un utente con questo numero.'})
    email_activated = models.BooleanField(default=False, auto_created=True)
    activation_token = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.user.username

    def get_image(self):
        if not (self.avatar and hasattr(self.avatar, 'url')):
            return settings.MEDIA_URL + 'placeholder/avatars/user.png'
        else:
            return self.avatar.url


class Business(models.Model):
    user = models.OneToOneField(User, related_name='business', on_delete=models.CASCADE)

    avatar = ResizedImageField(size=[250, 250], quality=95, crop=['middle', 'center'],
                               keep_meta=False, upload_to=content_file_name, blank=True, null=True)

    cf = models.CharField(max_length=16, unique=True)
    birth_date = models.DateField()
    city = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=150, blank=False)
    n_civ = models.CharField(max_length=10, blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    phone = PhoneNumberField(unique=True, error_messages={'unique': 'Esiste già un utente con questo numero.'})
    email_activated = models.BooleanField(default=False, auto_created=True)

    activation_token = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.user.username

    def get_cf(self):
        return self.cf.upper()

    def get_image(self):
        if not (self.avatar and hasattr(self.avatar, 'url')):
            return settings.MEDIA_URL + 'placeholder/avatars/user.png'
        else:
            return self.avatar.url

    class Meta:
        verbose_name_plural = "Businesses"
