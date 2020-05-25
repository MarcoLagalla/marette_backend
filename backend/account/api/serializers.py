from django.contrib.auth import validators
from django.contrib.auth.models import update_last_login
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from backend.account.models import Customer, Business
from django.db import transaction
from django.core import exceptions
from codicefiscale import isvalid as cf_isvalid

from ..models import User
from .validators import SetCustomErrorMessagesMixin
from ..tokens import account_activation_token


class CustomerSerializer(SetCustomErrorMessagesMixin, serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',
                                     validators=[UniqueValidator(queryset=User.objects.all())],)
    email = serializers.EmailField(source='user.email',
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    password = serializers.CharField(source='user.password', write_only=True)
    password2 = serializers.CharField(style={'input_style': 'password'}, write_only=True)

    birth_date = serializers.CharField(required=False)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)

    id = serializers.IntegerField(source='user.id', read_only=True)

    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name',
                  'birth_date', 'phone', 'email_activated', 'is_superuser', 'avatar']
        custom_error_messages_for_validators = {
            'username': {UniqueValidator: 'Esiste già un utente con questo username.'},
            'email': {UniqueValidator: 'Esiste già un utente con questa email.'},
            'phone': {UniqueValidator: 'Esiste già un utente con questo numero.'},
        }

    def to_representation(self, instance):
        my_fields = {'avatar'}
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                    data[field] = instance.get_image()
            except KeyError:
                pass
        return data

    @transaction.atomic
    def save(self):
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']

        user = User.objects.create(**self.validated_data['user'])

        if password != password2:
            raise serializers.ValidationError({'password': ['Le password devono combaciare.']})

        try:
            # validate the password and catch the exception
            validate_password(password=password, user=user)

            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors = dict()
            errors['password'] = list(e.messages)
            raise serializers.ValidationError(errors)


        user.set_password(password)
        user.save()
        update_last_login(None, user)

        del self.validated_data['user']
        del self.validated_data['password2']

        activation_token = account_activation_token.make_token(user)

        customer = Customer.objects.create(user=user, activation_token=activation_token, **self.validated_data)
        return customer


class BusinessSerializer(SetCustomErrorMessagesMixin, serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(source='user.email',
                                  validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(source='user.password', write_only=True)
    password2 = serializers.CharField(style={'input_style': 'password'}, write_only=True)

    id = serializers.IntegerField(source='user.id', read_only=True)

    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Business
        fields = ['id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'avatar',
                  'cf', 'birth_date', 'city', 'address', 'n_civ', 'cap', 'phone', 'email_activated']
        custom_error_messages_for_validators = {
            'username': {UniqueValidator: 'Esiste già un utente con questo username.'},
            'email': {UniqueValidator: 'Esiste già un utente con questa email.'},
            'cf': {UniqueValidator: 'Esiste già un utente con questo codice fiscale.'},
            'phone': {UniqueValidator: 'Esiste già un utente con questo numero.'},
            'birth_date': {RegexValidator: 'prova'},
        }

    def to_representation(self, instance):
        my_fields = {'avatar'}
        data = super().to_representation(instance)
        for field in my_fields:
            if field == 'avatar':
                try:
                        data[field] = instance.get_image()
                except KeyError:
                    pass
            elif field == 'cf':
                try:
                        data[field] = instance.get_cf()
                except KeyError:
                    pass
        return data

    @transaction.atomic
    def save(self):
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']
        cf = str(self.validated_data['cf']).upper()

        user = User.objects.create(**self.validated_data['user'])
        if password != password2:
            raise serializers.ValidationError({'password': ['Le password devono combaciare.']})

        try:
            # validate the password and catch the exception
            validate_password(password=password, user=user)

            # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors = dict()
            errors['password'] = list(e.messages)
            raise serializers.ValidationError(errors)

        if not cf_isvalid(cf):
            raise serializers.ValidationError({'cf': ['Il codice fiscale non è valido.']})

        user.set_password(password)
        user.save()
        update_last_login(None, user)

        del self.validated_data['user']
        del self.validated_data['password2']
        del self.validated_data['cf']

        activation_token = account_activation_token.make_token(user)

        business = Business.objects.create(user=user, activation_token=activation_token,
                                           cf=cf, **self.validated_data)
        return business


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    token = serializers.CharField()

class AskResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
