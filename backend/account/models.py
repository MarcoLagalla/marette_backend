from django.db import models
from django.core import validators as valids
import unidecode, re
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

    birth_date = models.DateField(blank=True, null=True)
    phone = PhoneNumberField(unique=True)

    def __str__(self):
        return self.user.username


class Business(models.Model):
    user = models.OneToOneField(User, related_name='business', on_delete=models.CASCADE)

    cf = models.CharField(max_length=16, unique=True)
    birth_date = models.DateField()
    city = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=150, blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    phone = PhoneNumberField(unique=True)

    def __str__(self):
        return self.user.username

    def get_url(self, name):  # eliminate "'", "^", "-", " ", "_", replace strange character and so
        url = unidecode.unidecode(name)  # .normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
        url = re.sub('[^0-9a-zA-Z]', '', url)
        url = ''.join(url.split()).lower()
        return url[:30]

    class Meta:
        verbose_name_plural = "Businesses"
