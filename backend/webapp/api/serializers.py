from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from ..models import Restaurant
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
        return restaurant
