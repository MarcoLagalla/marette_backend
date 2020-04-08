from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..models import Restaurant
from ...account.models import Business
from ...account.api.serializers import BusinessSerializer
from django.db import transaction

class RestaurantSerializer(serializers.ModelSerializer):
    pass
#     business = BusinessSerializer(many=True, read_only=True)
#     url = serializers.CharField(source='business.url')
#
#     class Meta:
#         model = Restaurant
#         fields = ['business', 'url', 'activity_name', 'activity_description', 'city', 'address', 'cap']


class CreateRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'url', 'activity_name', 'activity_description', 'city',
                  'address', 'cap', 'restaurant_number', 'p_iva']

    @transaction.atomic
    def save(self):
        business_user = self.context.get("business_user")

        restaurant = Restaurant.objects.create(owner=business_user,
                                               activity_name=self.validated_data['activity_name'],
                                               activity_description=self.validated_data['activity_description'],
                                               url=self.validated_data['url'],
                                               city=self.validated_data['city'],
                                               address=self.validated_data['address'],
                                               cap=self.validated_data['cap'],
                                               restaurant_number=self.validated_data['restaurant_number'],
                                               p_iva=self.validated_data['p_iva']  # todo validate p_iva
                                               )
        return restaurant
