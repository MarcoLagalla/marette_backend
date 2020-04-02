from django.db import models
from django.core import validators as valids
from django.utils.translation import ugettext_lazy as _
from backend.settings import dev as settings
import unidecode, re   #pip install unidecode
# Create your models here.
from django.contrib.auth.models import User


class CustomerUser(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    cellphone_number = models.CharField(max_length=13, blank=True, unique=True,
                                        validators=[valids.RegexValidator(regex='^(\+\d{2}){0,1}3{1}\d{9}$',
                                              message=_('Please insert a valid cellphone number'))])


    def __str__(self):
        return self.username

class BusinessUser(models.Model):
    # TODO: serve un campo description per la descrizione della attività
    objects = models.Manager()

    url = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=30, unique=True, blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100, blank=False)
    cap = models.IntegerField(validators=[valids.RegexValidator(regex='[0-9]{5}')])
    business_number = models.CharField(max_length=13, unique=True, validators=[
                        valids.RegexValidator(regex='^(\+\d{2}){0,1}3{1}\d{9}$',
                                              message=_('Please insert a valid cellphone number'))])

    def get_url(self, name):  # eliminate "'", "^", "-", " ", "_", replace strange character and so
        url = unidecode.unidecode(name)  # .normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
        url = re.sub('[^0-9a-zA-Z]', '', url)
        url = ''.join(url.split()).lower()
        return url[:30]