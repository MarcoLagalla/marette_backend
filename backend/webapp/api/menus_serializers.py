from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404

from ..models import Menu, MenuEntry, Product
from .products_serializers import ProductTagSerializer


class MenuEntryProductSerializer(serializers.ModelSerializer):
    tags = ProductTagSerializer(many=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image', 'tags')


class MenuEntrySerializer(serializers.ModelSerializer):
    products = MenuEntryProductSerializer(many=True)

    class Meta:
        model = MenuEntry
        fields = ('id', 'name', 'num_products', 'products')


class MenuSerializer(serializers.ModelSerializer):
    entries = MenuEntrySerializer(many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'price', 'entries')


