from django.db import models
from django.core import validators as valids
from django.utils.translation import ugettext_lazy as _
from backend.settings import dev as settings
import unidecode, re   #pip install unidecode

# Create your models here.


class CustomerUser(models.Model):
    base_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=False)
    cellphone_number = models.CharField(max_length=13, unique=True, validators=[
                        valids.RegexValidator(regex='^(\+\d{2}){0,1}3{1}\d{9}$',
                                              message=_('Please insert a valid cellphone number'))])


class BusinessUser(models.Model):
    # TODO: serve un campo description per la descrizione della attività
    objects = models.Manager()

    url = models.CharField(max_length=30, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', on_delete=models.CASCADE)
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
