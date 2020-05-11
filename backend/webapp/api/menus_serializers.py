from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404

from ..models.models import Product
from ..models.menu import Menu, MenuEntry
from .products_serializers import ProductTagSerializer


class MenuEntryProductSerializer(serializers.ModelSerializer):
    tags = ProductTagSerializer(many=True)
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image', 'tags')

    def get_image(self, obj):
        return obj.get_image()


class MenuEntrySerializer(serializers.ModelSerializer):
    products = MenuEntryProductSerializer(many=True)

    class Meta:
        model = MenuEntry
        fields = ('id', 'restaurant', 'menu', 'name', 'num_products', 'products')


class WriteMenuEntrySerializer(serializers.ModelSerializer):
    products = serializers.ListField(required=False)

    class Meta:
        model = MenuEntry
        fields = ('id', 'name', 'num_products', 'products')

    @transaction.atomic()
    def save(self, restaurant, menu):
        try:
            products = self.validated_data.pop('products')
        except KeyError:
            products = None

        menu_entry = MenuEntry.objects.create(restaurant=restaurant,
                                              menu=menu,
                                              **self.validated_data)

        if products:
            # se ho dei Prodotti di QUESTO RISTORANTE
            for itm in products:
                try:
                    t = Product.objects.all().filter(restaurant=restaurant).get(id=itm)
                    # TODO: secondo me va bene anche cosi, nello store non è disponibile
                    #       se già non lo era, ma nel menu si vede.
                    # if not t.available:
                    #     t.available = True
                    #     t.save()
                    menu_entry.products.add(t)
                except Product.DoesNotExist:
                    pass

        # salvo le modifiche
        menu_entry.save()

        return menu_entry


class MenuSerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'price', 'entries')

    def get_entries(self, obj):
        return MenuEntrySerializer(obj.get_entries(), many=True).data


class WriteMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'description', 'price')

    @transaction.atomic()
    def save(self, restaurant):

        menu = Menu.objects.create(restaurant=restaurant, **self.validated_data)
        menu.save()

        return menu