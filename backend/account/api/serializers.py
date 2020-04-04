from django.contrib.auth.models import update_last_login
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from backend.account.models import Customer, Business
from django.db import transaction
from codicefiscale import isvalid as cf_isvalid

from ..models import User


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(source='user.email',
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(source='user.password', write_only=True)
    password2 = serializers.CharField(style={'input_style': 'password'}, write_only=True)

    birth_date = serializers.CharField(required=False)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name',
                  'birth_date', 'phone', 'is_active', 'is_superuser']

    @transaction.atomic
    def save(self):
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']

        user = User.objects.create(**self.validated_data['user'])

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})
        user.set_password(password)
        user.is_active = False
        user.save()
        update_last_login(None, user)

        del self.validated_data['user']
        del self.validated_data['password2']

        customer = Customer.objects.create(user=user, **self.validated_data)
        return customer


class BusinessSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.CharField(source='user.email',
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(source='user.password', write_only=True)
    password2 = serializers.CharField(style={'input_style': 'password'}, write_only=True)

    class Meta:
        model = Business
        fields = ['id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name',
                  'cf', 'birth_date', 'city', 'address', 'cap', 'phone']

    @transaction.atomic
    def save(self):
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']
        cf = self.validated_data['cf']

        user = User.objects.create(**self.validated_data['user'])

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match!'})

        if not cf_isvalid(cf):
            raise serializers.ValidationError({'cf' : 'not valid'})

        user.set_password(password)
        user.is_active = False
        user.save()
        update_last_login(None, user)

        del self.validated_data['user']
        del self.validated_data['password2']

        business = Business.objects.create(user=user, **self.validated_data)
        return business


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField()

class AskResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value