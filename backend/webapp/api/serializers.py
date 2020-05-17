from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator, ValidationError
from ..models.models import Restaurant, RestaurantDiscount, Picture
from ..models.components import RestaurantComponents, HomeComponent, VetrinaComponent, GalleriaComponent, \
    EventiComponent, MenuComponent, ContattaciComponent

from ...account.api.serializers import BusinessSerializer
from django.db import transaction, IntegrityError
from django.utils.text import slugify
from localflavor.it.util import vat_number_validation


class PictureSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Picture
        fields = ('id', 'name', 'description', 'image')

    @transaction.atomic
    def save(self, restaurant=None, **kwargs):
        if restaurant:
            try:

                picture = Picture.objects.create(restaurant=restaurant, **self.validated_data)
                return picture

            except Exception as err:
                raise serializers.ValidationError({'error': err})

        return None


class RestaurantDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDiscount
        fields = ('id', 'title', 'category', 'type', 'value', )

    @transaction.atomic
    def save(self, restaurant):
        try:

            restaurant_discount = RestaurantDiscount.objects.create(
                restaurant=restaurant,
                **self.validated_data
            )
        except IntegrityError:
            raise serializers.ValidationError({'error': 'Questo sconto esiste già.'})

        return restaurant_discount


class ListRestaurantSerializer(serializers.ModelSerializer):
    business = BusinessSerializer(many=True, read_only=True)
    discounts = RestaurantDiscountSerializer(many=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['business', 'id', 'slug', 'url', 'activity_name', 'activity_description', 'image',
                  'city', 'address', 'n_civ', 'cap', 'restaurant_number', 'p_iva', 'discounts']

    def get_image(self, obj):
        return obj.get_image()


class CreateRestaurantSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Restaurant
        fields = ['id', 'activity_name', 'activity_description', 'city', 'image',
                  'address', 'n_civ', 'cap', 'restaurant_number', 'p_iva']

    @transaction.atomic
    def save(self, owner):

        try:
            if not vat_number_validation(self.validated_data['p_iva']):
                raise serializers.ValidationError({'p_iva': 'La partita iva non è valida'})
        except Exception:
            raise serializers.ValidationError({'p_iva': 'La partita iva non è valida'})


        restaurant = Restaurant.objects.create(owner=owner, **self.validated_data)
        restaurant.set_url()  # needed to have /id_restaurant/name_restaurant
        restaurant.save()


        # create ComponentsPanels (empty)
        home = HomeComponent.objects.create(restaurant=restaurant, name='HOME')
        vetrina = VetrinaComponent.objects.create(restaurant=restaurant, name='VETRINA')
        galleria = GalleriaComponent.objects.create(restaurant=restaurant, name='GALLERIA')
        eventi = EventiComponent.objects.create(restaurant=restaurant, name='EVENTI')
        menu = MenuComponent.objects.create(restaurant=restaurant, name='MENU')
        contattaci = ContattaciComponent.objects.create(restaurant=restaurant, name='CONTATTACI')

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
    image = serializers.SerializerMethodField(required=False)
    name = serializers.SerializerMethodField()

    class Meta:
        model = HomeComponent
        fields = ('id', 'show', 'name', 'description', 'image')

    def get_image(self, instance):
        return instance.get_image()

    def get_name(self, instance):
        return instance.get_name()


class VetrinaSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = VetrinaComponent
        fields = ('id', 'name', 'menu_giorno', 'show')

    def get_name(self, instance):
        return instance.get_name()


class MenuSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = MenuComponent
        fields = ('id', 'name', 'show')

    def get_name(self, instance):
        return instance.get_name()


class GalleriaSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    immagini = serializers.SerializerMethodField()

    class Meta:
        model = GalleriaComponent
        fields = ('id', 'name', 'immagini', 'show')

    def get_name(self, instance):
        return instance.get_name()

    def get_immagini(self, instance):
        return PictureSerializer(instance.get_images(), many=True).data


class EventiSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = EventiComponent
        fields = ('id', 'name', 'show')

    def get_name(self, instance):
        return instance.get_name()


class ContattaciSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ContattaciComponent
        fields = ('id', 'name', 'show')

    def get_name(self, instance):
        return instance.get_name()


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



