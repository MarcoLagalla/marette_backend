from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from backend.account.models import Customer, Business

from ..models import User


class CustomerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_superuser = serializers.BooleanField(source='user.is_superuser')

    class Meta:
        model = Customer
        fields = ['user', 'username', 'email', 'first_name', 'last_name',
                  'birth_date', 'cellphone_number', 'is_superuser']


class BusinessSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_superuser = serializers.BooleanField(source='user.is_superuser')

    class Meta:
        model = Business
        fields = ['user', 'username', 'email', 'first_name', 'last_name',
                  'url', 'activity_name', 'activity_description', 'city',
                  'address', 'cap', 'business_number', 'is_superuser']


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

        try:
            first_name = self.validated_data['user']['first_name']
        except KeyError:
            first_name = ''

        try:
            last_name = self.validated_data['user']['last_name']
        except KeyError:
            last_name = ''

        try:
            birth_date = self.validated_data['birth_date']
        except KeyError:
            birth_date = ''

        try:
            cellphone_number = self.validated_data['cellphone_number']
        except KeyError:
            cellphone_number = ''

        user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.is_active = False
        user.save()

        customer = Customer.objects.create(user=user,
                                           birth_date=birth_date,
                                           cellphone_number=cellphone_number)
        return customer


class BusinessRegistationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(source='user.email',
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    password = serializers.CharField(source='user.password', write_only=True)
    password2 = serializers.CharField(style={'input_style': 'password'}, write_only=True)

    class Meta:
        model = Business
        fields = ['id', 'username', 'password', 'password2','email', 'first_name', 'last_name',
                  'url', 'activity_name', 'activity_description', 'city',
                  'address', 'cap', 'business_number']

    def save(self):
        username = self.validated_data['user']['username']
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']
        email = self.validated_data['user']['email']
        first_name = self.validated_data['user']['first_name']
        last_name = self.validated_data['user']['last_name']

        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.save()

        business = Business.objects.create(user=user,
                                           activity_name=self.validated_data['activity_name'],
                                           activity_description=self.validated_data['activity_description'],
                                           url=self.validated_data['url'],
                                           city=self.validated_data['city'],
                                           address=self.validated_data['address'],
                                           cap=self.validated_data['cap'],
                                           business_number=self.validated_data['business_number']
                                           )
        return business


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value