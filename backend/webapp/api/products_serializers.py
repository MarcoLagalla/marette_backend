from rest_framework import serializers
from django.db import transaction
from django.shortcuts import get_object_or_404

from ..models.models import Product, ProductDiscount, ProductTag


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = ('id', 'title', 'type', 'value', )


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'


class ReadProductSerializer(serializers.ModelSerializer):
    tags = ProductTagSerializer(many=True, required=False)
    discounts = ProductDiscountSerializer(many=True, required=False)
    final_price = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(required=False)
    thumb_image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'price',
                  'tags', 'discounts', 'final_price', 'image', 'thumb_image', 'show_image')

    def get_image(self, instance):
        return instance.get_image()

    def get_thumb_image(self, instance):
        return instance.get_thumb_image()

    def get_final_price(self, obj):
        return obj.get_price_with_discount()


class WriteProductSerializer(serializers.ModelSerializer):

    tags = serializers.ListField(required=False)
    discounts = serializers.ListField(required=False)
    image = serializers.ImageField(required=False)
    show_image = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price',
                  'tags', 'discounts', 'image', 'show_image')

    def get_image_url(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.get_image())

    @transaction.atomic()
    def save(self, restaurant):
        # i tags e i discounts sono oggetti a parte:
        try:
            tags_data = self.validated_data.pop('tags')
        except KeyError:
            tags_data = None

        try:
            discount_data = self.validated_data.pop('discounts')
        except KeyError:
            discount_data = None

        product = Product.objects.create(restaurant=restaurant, **self.validated_data)
        product.tags.clear()
        product.discounts.clear()

        if tags_data:
            # se ho dei ProductTags inseriti (id)
            for tag in tags_data:
                try:
                    t = ProductTag.objects.all().get(id=tag)
                    product.tags.add(t)
                except ProductTag.DoesNotExist:
                    pass

        if discount_data:
            # se ho dei Discount inseriti (id)
            for discount in discount_data:
                try:
                    d = ProductDiscount.objects.all().filter(restaurant=restaurant).get(id=discount)
                    product.discounts.add(d)
                except ProductDiscount.DoesNotExist:
                    pass

        # salvo le modifiche
        product.save()
        return product


