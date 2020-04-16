from django.contrib.auth.models import update_last_login
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from backend.account.models import Customer, Business
from django.db import transaction
from codicefiscale import isvalid as cf_isvalid

from ..models import User
from .validators import SetCustomErrorMessagesMixin


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
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)

    id = serializers.IntegerField(source='user.id', read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name',
                  'birth_date', 'phone', 'email_activated', 'is_superuser']
        custom_error_messages_for_validators = {
            'username': {UniqueValidator: 'Esiste già un utente con questo username.'},
            'email': {UniqueValidator: 'Esiste già un utente con questa email.'},
            'phone': {UniqueValidator: 'Esiste già un utente con questo numero.'},
        }

    @transaction.atomic
    def save(self):
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']

        user = User.objects.create(**self.validated_data['user'])

        if password != password2:
            raise serializers.ValidationError({'password': ['Le password devono combaciare.']})
        user.set_password(password)
        user.save()
        update_last_login(None, user)

        del self.validated_data['user']
        del self.validated_data['password2']

        customer = Customer.objects.create(user=user, **self.validated_data)
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

    class Meta:
        model = Business
        fields = ['id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name',
                  'cf', 'birth_date', 'city', 'address', 'n_civ', 'cap', 'phone', 'email_activated']
        custom_error_messages_for_validators = {
            'username': {UniqueValidator: 'Esiste già un utente con questo username.'},
            'email': {UniqueValidator: 'Esiste già un utente con questa email.'},
            'cf': {UniqueValidator: 'Esiste già un utente con questo codice fiscale.'},
            'phone': {UniqueValidator: 'Esiste già un utente con questo numero.'},
            'birth_date': {RegexValidator: 'prova'},
        }

    @transaction.atomic
    def save(self):
        password = self.validated_data['user']['password']
        password2 = self.validated_data['password2']
        cf = str(self.validated_data['cf']).upper()

        user = User.objects.create(**self.validated_data['user'])
        if password != password2:
            raise serializers.ValidationError({'password': ['Le password devono combaciare.']})

        if not cf_isvalid(cf):
            raise serializers.ValidationError({'cf': ['Il codice fiscale non è valido.']})

        user.set_password(password)
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
    new_password2 = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if not self.new_password == self.new_password2:
            raise serializers.ValidationError({'password': 'Le password devono combaciare'})
        validate_password(value)
        return value
