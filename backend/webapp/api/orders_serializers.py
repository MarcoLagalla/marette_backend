from rest_framework import serializers

from ..models.orders import Order, OrderMenuEntry, OrderProductEntry
from ..models.models import Customer, Restaurant, Product
from ..models.menu import Menu


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductEntry
        fields = '__all__'


class OrderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderMenuEntry
        fields = '__all__'


class ReadOrderSerializer(serializers.ModelSerializer):
    items = OrderProductSerializer(many=True)
    menus_items = OrderMenuSerializer(many=True)
    total = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    imposable = serializers.SerializerMethodField()
    iva = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'date_created', 'user', 'restaurant', 'items', 'menus_items',
                  'total', 'discount', 'imposable', 'iva')

    def get_total(self, obj):
        return obj.get_total()

    def get_discount(self, obj):
        return obj.get_total_discount()

    def get_imposable(self, obj):
        return str(obj.get_imposable())

    def get_iva(self, obj):
        return obj.get_total_iva()


class OrderSerializer(serializers.ModelSerializer):

    items = OrderProductSerializer(many=True, required=False)
    menus_items = OrderMenuSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'date_created', 'user', 'restaurant', 'items', 'menus_items')

    def validate(self, attrs):

        val_errors = {}
        try:
            user = attrs.get('user', None)
            try:
                user = Customer.objects.all().get(id=user.id)
            except Customer.DoesNotExist:
                val_errors['user'] = "L'utente non esiste"
        except KeyError:
            pass

        rest = attrs.get('restaurant', None)
        rest = Restaurant.objects.all().get(id=rest.id)

        try:
            items = attrs.get('items', [])

            for item in items:
                try:
                    prodotto = Product.objects.all().filter(restaurant=rest).get(id=item['product'].id)
                except Product.DoesNotExist:
                    raise serializers.ValidationError({'error': 'Prodotto ' + item['product'] + ' non trovato'})
        except KeyError:
            items = []

        try:
            menu_items = attrs.get('menu_items', [])
            for item in menu_items:
                try:
                    menu = Menu.objects.all().filter(restaurant=rest).get(id=item['menu'].id)
                except Menu.DoesNotExist:
                    raise serializers.ValidationError({'error': f'Menu ' + item['menu'] + ' non trovato'})
        except KeyError:
            menu_items = []

        if len(items) == 0 and len(menu_items) == 0:
            raise serializers.ValidationError({'error': 'Impossibile creare un ordine senza prodotti'})

        if len(val_errors.keys()) != 0:
            raise serializers.ValidationError(val_errors)

        return attrs

    def save(self, **kwargs):
        items = self.validated_data.get('items', None)
        menus_items = self.validated_data.get('menus_items', None)

        order = Order.objects.create(restaurant=self.validated_data['restaurant'],
                                     user=self.validated_data['user'])

        if items:
            for item in items:
                pe = OrderProductEntry.objects.create(product=item['product'], quantity=item['quantity'])
                order.items.add(pe)

        if menus_items:
            for item in menus_items:
                pe = OrderMenuEntry.objects.create(menu=item['menu'], quantity=item['quantity'])
                order.menus_items.add(pe)

        order.save()
        return order
