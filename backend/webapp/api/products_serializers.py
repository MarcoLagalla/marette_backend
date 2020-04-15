from rest_framework import serializers
from django.db import transaction

from ..models import Product, ProductDiscount, ProductTag


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = ('title', )


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        exclude = ('id', )


class ReadProductSerializer(serializers.ModelSerializer):
    tags = ProductTagSerializer(many=True, required=False)
    discounts = ProductDiscountSerializer(many=True, required=False)
    final_price = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price',
                  'tags', 'discounts', 'final_price', 'image')

    def get_image_url(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.get_image())

    def get_final_price(self, obj):
        return obj.get_price_with_discount()


class WriteProductSerializer(serializers.ModelSerializer):

    tags = serializers.ListField(required=False)
    discounts = serializers.ListField(required=False)

    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price',
                  'tags', 'discounts', 'image')

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