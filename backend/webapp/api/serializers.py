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
        fields = ['business', 'url', 'activity_name', 'activity_description', 'city', 'address', 'n_civ', 'cap']


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

        restaurant = Restaurant.objects.create(owner=business_user,
                                               activity_name=self.validated_data['activity_name'],
                                               activity_description=self.validated_data['activity_description'],
                                               url=slugify(self.validated_data['activity_name']),               # todo /ID_BUSINESS/bouvette
                                               city=self.validated_data['city'],
                                               address=self.validated_data['address'],
                                               n_civ=self.validated_data['n_civ'],
                                               cap=self.validated_data['cap'],
                                               restaurant_number=self.validated_data['restaurant_number'],
                                               p_iva=self.validated_data['p_iva'])
        return restaurant
