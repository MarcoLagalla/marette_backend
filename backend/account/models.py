from django.db import models
from django.core import validators as valids
import unidecode, re
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

    birth_date = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(unique=True, error_messages={'unique': 'Esiste già un utente con questo numero.'})
    email_activated = models.BooleanField(default=False, auto_created=True)

    def __str__(self):
        return self.user.username


class Business(models.Model):
    user = models.OneToOneField(User, related_name='business', on_delete=models.CASCADE)

    cf = models.CharField(max_length=16, unique=True)
    birth_date = models.DateField()
    city = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=150, blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    phone = PhoneNumberField(unique=True, error_messages={'unique': 'Esiste già un utente con questo numero.'})
    email_activated = models.BooleanField(default=False, auto_created=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Businesses"
