from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from django.db import transaction
from .serializers import ListRestaurantSerializer, CreateRestaurantSerializer
from ..models import Restaurant
from ...account.models import Business
from ...account.permissions import IsBusiness
import phonenumbers
import re
from localflavor.it.util import vat_number_validation



class ListRestaurantsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Restaurant.objects.all()
    serializer_class = ListRestaurantSerializer


class CreateRestaurantAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness]

    # only authenticated business users can create a new restaurant
    def post(self, request):
        user = get_object_or_404(Business, user=self.request.user)
        data = {}
        if user:
            serializer = CreateRestaurantSerializer(data=request.data, context={'business_user': user})
            if serializer.is_valid():
                restaurant = serializer.save()
                data['response'] = "successfully registered a new restaurant"
                data['id_restaurant'] = restaurant.id
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data['response'] = isinstance(user, Business)
        return Response(data, status=status.HTTP_403_FORBIDDEN)


class ShowRestaurantAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, slug):
        restaurant = get_object_or_404(Restaurant, id=id)
        try:
            data = {}
            serializer = ListRestaurantSerializer(restaurant, many=False)
            data.update(serializer.data)
            return Response(data, status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({'error': ["Ristorante non trovato."]}, status.HTTP_404_NOT_FOUND)


class UpdateRestaurantAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, slug):
        try:
            restaurant = get_object_or_404(Restaurant, id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': ["Ristorante non trovato."]}, status.HTTP_404_NOT_FOUND)

        missing_keys = False
        value_errors = {}

        try:
            activity_name = request.data.pop('activity_name')
        except KeyError:
            missing_keys = True
            value_errors.update({'activity_name': 'Il campo non può essere vuoto.'})

        try:
            activity_description = request.data.pop('activity_description')
        except KeyError:
            missing_keys = True
            value_errors.update({'activity_description': 'Il campo non può essere vuoto.'})

        try:
            restaurant_number = request.data.pop('restaurant_number')
        except KeyError:
            missing_keys = True
            value_errors.update({'restaurant_number': 'Il campo non può essere vuoto.'})

        try:
            city = request.data.pop('city')
        except KeyError:
            missing_keys = True
            value_errors.update({'city': 'Il campo non può essere vuoto.'})

        try:
            address = request.data.pop('address')
        except KeyError:
            missing_keys = True
            value_errors.update({'address': 'Il campo non può essere vuoto.'})

        try:
            n_civ = request.data.pop('n_civ')
        except KeyError:
            missing_keys = True
            value_errors.update({'n_civ': 'Il campo non può essere vuoto.'})

        try:
            cap = request.data.pop('cap')
        except KeyError:
            missing_keys = True
            value_errors.update({'cap': 'Il campo non può essere vuoto.'})

        try:
            p_iva = request.data.pop('p_iva')
        except KeyError:
            missing_keys = True
            value_errors.update({'p_iva': 'Il campo non può essere vuoto.'})

        if missing_keys:
            return Response(value_errors, status=status.HTTP_400_BAD_REQUEST)

        validation_errors_ = False
        validation_errors = {}
        if not phonenumbers.is_valid_number(phonenumbers.parse(restaurant_number, "IT")):
            validation_errors_ = True
            validation_errors.update({'restaurant_number': 'Il numero di telefono deve essere valido'})

        cap_validator = re.match('^[0-9]{5}$', cap)
        if not cap_validator:
            validation_errors_ = True
            validation_errors.update({'cap': 'Inserire un CAP valido.'})

        if not vat_number_validation(p_iva):
            validation_errors_ = True
            validation_errors.update({'p_iva': 'La partita iva non è valida'})

        if validation_errors_:
            return Response(validation_errors, status=status.HTTP_400_BAD_REQUEST)

        if request.user == restaurant.owner.user:
            # campi che possono essere modificati:
            # nome_attività, descrizione_attività, p_iva
            # numero di telefono del ristorante, city, address, cap
            restaurant.activity_name = activity_name
            restaurant.activity_description = activity_description

            restaurant.city = city
            restaurant.address = address
            restaurant.n_civ = n_civ
            restaurant.cap = cap
            restaurant.restaurant_number = restaurant_number
            restaurant.p_iva = p_iva

            restaurant.save()
            restaurant.set_url()  # needed to update the url if activity_name changes
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
