from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404

from ..models.models import Product
from ..models.orders import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'date_created', 'status', 'user', 'restaurant', 'items',
                  'menus_items', 'code', 'valid')

    def user(self, obj):
        return obj.get_user()

    def restaurant(self, obj):
        return obj.get_restaurant()
