from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from backend.account.models import Customer

from ..models import User


class CustomerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_superuser = serializers.BooleanField(source='user.is_superuser')

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'birth_date', 'cellphone_number', 'is_superuser']


class CustomerRegistationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(source='user.email',
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    password = serializers.CharField(source='user.password', write_only=True)
    password2 = serializers.CharField(style={'input_style': 'password'}, write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name',
                  'birth_date', 'cellphone_number']

    def save(self):
        username = self.validated_data['user']['username']
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']
        email = self.validated_data['user']['email']
        first_name = self.validated_data['user']['first_name']
        last_name = self.validated_data['user']['last_name']

        user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.save()

        customer = Customer.objects.create(user=user,
                                           birth_date=self.validated_data['birth_date'],
                                           cellphone_number=self.validated_data['cellphone_number'])
        return customer


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()