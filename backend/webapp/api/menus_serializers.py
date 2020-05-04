from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404

from ..models.models import Product
from ..models.menu import Menu, MenuEntry
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


class WriteMenuEntrySerializer(serializers.ModelSerializer):
    products = serializers.ListField(required=False)

    class Meta:
        model = MenuEntry
        fields = ('id', 'name', 'num_products', 'products')

    @transaction.atomic()
    def save(self, restaurant):
        try:
            products = self.validated_data.pop('products')
        except KeyError:
            products = None

        menu_entry = MenuEntry.objects.create(restaurant=restaurant, **self.validated_data)

        if products:
            # se ho dei MenuEntry di QUESTO RISTORANTE
            for itm in products:
                try:
                    t = Product.objects.all().filter(restaurant=restaurant).get(id=itm)
                    menu_entry.products.add(t)
                except Product.DoesNotExist:
                    pass

        # salvo le modifiche
        menu_entry.save()

        return menu_entry


class MenuSerializer(serializers.ModelSerializer):
    entries = MenuEntrySerializer(many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'price', 'entries')


class MenuSerializer(serializers.ModelSerializer):
    entries = MenuEntrySerializer(many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'price', 'entries')


class WriteMenuSerializer(serializers.ModelSerializer):
    entries = serializers.ListField(required=False)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'price', 'entries')

    @transaction.atomic()
    def save(self, restaurant):
        # i tags e i discounts sono oggetti a parte:
        try:
            entries = self.validated_data.pop('entries')
        except KeyError:
            entries = None

        menu = Menu.objects.create(restaurant=restaurant, **self.validated_data)

        if entries:
            # se ho dei MenuEntry di QUESTO RISTORANTE
            for itm in entries:
                try:
                    t = MenuEntry.objects.all().filter(restaurant=restaurant).get(id=itm)
                    menu.entries.add(t)
                except MenuEntry.DoesNotExist:
                    pass

        # salvo le modifiche
        menu.save()

        return menu