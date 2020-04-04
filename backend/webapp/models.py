from django.core import validators as valids
from django.db import models
import unidecode, re
from localflavor.it.util import vat_number_validation
from phonenumber_field.modelfields import PhoneNumberField
from backend.account.models import Business


class Restaurant(models.Model):
    owner = models.ForeignKey(Business, related_name='restaurant', on_delete=models.CASCADE)
    url = models.CharField(max_length=30, unique=True, blank=False)
    activity_name = models.CharField(max_length=30, unique=False, blank=False)
    activity_description = models.TextField(blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')], blank=False)
    restaurant_number = PhoneNumberField(null=False, blank=False, help_text='Contact phone number')
    p_iva = models.CharField(max_length=11, blank=False, unique=True, validators=[vat_number_validation])



    # products =               # todo fai in seguito
    # menus =
    # etc ...


    def __str__(self):
        return self.activity_name


    def get_url(self, name):  # eliminate "'", "^", "-", " ", "_", replace strange character and so
        url = unidecode.unidecode(name)  # .normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
        url = re.sub('[^0-9a-zA-Z]', '', url)
        url = ''.join(url.split()).lower()
        return url[:30]



#
# class Product(models.Model):
#     product_id = models.PositiveIntegerField(default=0)
#     #activity = models.ForeignKey(BusinessUser, related_name='activity', on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#     description = models.TextField(max_length=600)
#     #food_type = forms.ChoiceField(choices=FOOD_CATEGORY, widget=forms.RadioSelect())
#     price = models.DecimalField(decimal_places=2, max_digits=5, validators=[valids.MinValueValidator(0.10)])
#     vegetarian = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
