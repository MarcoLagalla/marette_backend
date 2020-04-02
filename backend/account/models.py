from django.db import models
from django.core import validators as valids
import unidecode, re
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    cellphone_number = PhoneNumberField(blank=True, help_text='Contact phone number', unique=True)

    def __str__(self):
        return self.user.username


class Business(models.Model):
    user = models.OneToOneField(User, related_name='business', on_delete=models.CASCADE)

    url = models.CharField(max_length=30, unique=True)
    activity_name = models.CharField(max_length=30, unique=True, blank=False)
    activity_description = models.TextField()
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')])
    business_number = PhoneNumberField(blank=False, help_text='Contact phone number')

    def __str__(self):
        return self.activity_name

    def get_url(self, name):  # eliminate "'", "^", "-", " ", "_", replace strange character and so
        url = unidecode.unidecode(name)  # .normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
        url = re.sub('[^0-9a-zA-Z]', '', url)
        url = ''.join(url.split()).lower()
        return url[:30]

    class Meta:
        verbose_name_plural = "Businesses"