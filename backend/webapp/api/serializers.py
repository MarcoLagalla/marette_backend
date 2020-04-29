from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from ..models import Restaurant, RestaurantComponents, HomeComponent, VetrinaComponent, GalleriaComponent, \
    EventiComponent, MenuComponent, ContattaciComponent

from ...account.models import Business
from ...account.api.serializers import BusinessSerializer
from django.db import transaction
from django.utils.text import slugify
from localflavor.it.util import vat_number_validation


class ListRestaurantSerializer(serializers.ModelSerializer):
    business = BusinessSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ['business', 'id', 'slug', 'url', 'activity_name', 'activity_description', 'city', 'address', 'n_civ', 'cap']


class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'activity_name', 'activity_description', 'city',
                  'address', 'n_civ', 'cap', 'restaurant_number', 'p_iva']

    @transaction.atomic
    def save(self):
        business_user = self.context.get("business_user")

        try:
            if not vat_number_validation(self.validated_data['p_iva']):
                raise serializers.ValidationError({'p_iva': 'La partita iva non è valida'})
        except Exception:
            raise serializers.ValidationError({'p_iva': 'La partita iva non è valida'})

        restaurant = Restaurant.objects.create(owner=business_user, **self.validated_data)
        restaurant.set_url()  # needed to have /id_restaurant/name_restaurant
        restaurant.save()

        # create ComponentsPanels (empty)
        home = HomeComponent.objects.create(restaurant=restaurant, name='Home')
        vetrina = VetrinaComponent.objects.create(restaurant=restaurant, name='Vetrina')
        galleria = GalleriaComponent.objects.create(restaurant=restaurant, name='Galleria')
        eventi = EventiComponent.objects.create(restaurant=restaurant, name='Eventi')
        menu = MenuComponent.objects.create(restaurant=restaurant, name='Menu')
        contattaci = ContattaciComponent.objects.create(restaurant=restaurant, name='Menu')

        RestaurantComponents.objects.create(
            restaurant=restaurant,
            home=home,
            vetrina=vetrina,
            galleria=galleria,
            eventi=eventi,
            menu=menu,
            contattaci=contattaci
        )

        return restaurant


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeComponent
        fields = ('id', 'show')
class VetrinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VetrinaComponent
        fields = ('id', 'show')
class MenuSerializer(serializers.ModelSerializer):
            class Meta:
                model = MenuComponent
                fields = ('id', 'show')
class GalleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleriaComponent
        fields = ('id', 'show')
class EventiSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventiComponent
        fields = ('id', 'show')
class ContattaciSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventiComponent
        fields = ('id', 'show')

class RestaurantComponentsSerializer(serializers.ModelSerializer):
    home = HomeSerializer()
    vetrina = VetrinaSerializer()
    menu = MenuSerializer()
    galleria = GalleriaSerializer()
    eventi = EventiSerializer()
    contattaci = ContattaciSerializer()

    class Meta:
        model = RestaurantComponents
        fields = ('home', 'vetrina', 'menu', 'galleria', 'eventi', 'contattaci')
