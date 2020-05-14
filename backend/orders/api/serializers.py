from rest_framework import serializers
from ..models import OrderNotification


class OrderNotificationSerialzier(serializers.ModelSerializer):
    class Meta:
        model = OrderNotification
        fields = '__all__'