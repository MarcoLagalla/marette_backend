from sys import path
import os
from django.conf import settings
from django.db import models
from django.core import validators as valids
import unidecode, re
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
import random
import string


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def content_file_name(instance, filename):
    name, ext = filename.split('.')
    file_path = 'avatars/{customer_id}/{rand}/avatar.{ext}'.format(
         customer_id=instance.user.id, rand=randomString(5), ext=ext)
    return file_path


class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

    avatar = ResizedImageField(size=[250, 250], quality=95, crop=['middle', 'center'],
                               keep_meta=False, upload_to=content_file_name, blank=True, null=True)

    birth_date = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(unique=True, error_messages={'unique': 'Esiste già un utente con questo numero.'})
    email_activated = models.BooleanField(default=False, auto_created=True)

    def __str__(self):
        return self.user.username

    def get_image(self):
        if not (self.avatar and hasattr(self.avatar, 'url')):
            return 'media/placeholder/avatars/user.png'
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
    n_civ = models.IntegerField(blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    phone = PhoneNumberField(unique=True, error_messages={'unique': 'Esiste già un utente con questo numero.'})
    email_activated = models.BooleanField(default=False, auto_created=True)

    def __str__(self):
        return self.user.username

    def get_image(self):
        if not (self.avatar and hasattr(self.avatar, 'url')):
            return 'media/placeholder/avatars/user.png'
        else:
            return self.avatar.url

    class Meta:
        verbose_name_plural = "Businesses"


# Remove empty avatar dirs

@receiver(post_save, sender=Business)
@receiver(post_save, sender=Customer)
def clean_empty_folder(sender, instance, **kwargs):
    for root, dirs, files in os.walk(os.path.join(settings.MEDIA_ROOT, 'avatars')):
        for d in dirs:
            dir = os.path.join(root, d)
            # check if dir is empty
            if not os.listdir(dir):
                os.rmdir(dir)