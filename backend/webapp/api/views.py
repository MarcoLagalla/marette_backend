import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.shortcuts import get_object_or_404
from django.db import transaction
from .serializers import ListRestaurantSerializer, CreateRestaurantSerializer, RestaurantComponentsSerializer
from ..models.models import Restaurant
from ..models.components import RestaurantComponents
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
    permission_classes = [IsAuthenticated, IsBusiness]

    # only authenticated business users can create a new restaurant
    @transaction.atomic()
    def post(self, request):
        try:
            user = Business.objects.all().get(user=self.request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = {}
        try:
            input_data = json.loads(request.data['data'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            image = request.FILES['image']
            input_data.update({'image': image})
        except Exception as err:
            pass

        if user:
            serializer = CreateRestaurantSerializer(data=input_data, context={'business_user': user})
            if serializer.is_valid():
                restaurant = serializer.save(user)
                data['response'] = "Ristorante correttamente creato"
                data['id_restaurant'] = restaurant.id
                data['slug'] = restaurant.slug
                data['image'] = restaurant.get_image()
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data['response'] = isinstance(user, Business)
        return Response(data, status=status.HTTP_403_FORBIDDEN)


class ShowRestaurantAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': ["Ristorante non trovato."]}, status.HTTP_404_NOT_FOUND)

        data = {}
        serializer = ListRestaurantSerializer(restaurant, many=False)
        data.update(serializer.data)

        # retrieve restaurant components
        try:
            components = RestaurantComponents.objects.get(restaurant=restaurant)
            components_data = RestaurantComponentsSerializer(components)
            data.update({'components': components_data.data})
        except RestaurantComponents.DoesNotExist:
            pass

        return Response(data, status.HTTP_200_OK)


class UpdateRestaurantAPIView(APIView):
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id):
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': ["Ristorante non trovato."]}, status.HTTP_404_NOT_FOUND)

        missing_keys = False
        value_errors = {}
        try:
            input_data = json.loads(request.data['data'])
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            image = request.FILES['image']
            input_data.update({'image': image})
        except Exception as err:
            input_data.update({'image': None})

        try:
            activity_name = input_data.get('activity_name')
        except KeyError:
            missing_keys = True
            value_errors.update({'activity_name': 'Il campo non può essere vuoto.'})

        try:
            activity_description = input_data.get('activity_description')
        except KeyError:
            missing_keys = True
            value_errors.update({'activity_description': 'Il campo non può essere vuoto.'})

        try:
            restaurant_number = input_data.get('restaurant_number')
        except KeyError:
            missing_keys = True
            value_errors.update({'restaurant_number': 'Il campo non può essere vuoto.'})

        try:
            city = input_data.get('city')
        except KeyError:
            missing_keys = True
            value_errors.update({'city': 'Il campo non può essere vuoto.'})

        try:
            address = input_data.get('address')
        except KeyError:
            missing_keys = True
            value_errors.update({'address': 'Il campo non può essere vuoto.'})

        try:
            n_civ = input_data.get('n_civ')
        except KeyError:
            missing_keys = True
            value_errors.update({'n_civ': 'Il campo non può essere vuoto.'})

        try:
            cap = input_data.get('cap')
        except KeyError:
            missing_keys = True
            value_errors.update({'cap': 'Il campo non può essere vuoto.'})

        try:
            p_iva = input_data.get('p_iva')
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

        cap_validator = re.match('^[0-9]{5}$', str(cap))
        if not cap_validator:
            validation_errors_ = True
            validation_errors.update({'cap': 'Inserire un CAP valido.'})

        try:
            if not vat_number_validation(p_iva):
                validation_errors_ = True
                validation_errors.update({'p_iva': 'La partita iva non è valida'})
        except Exception:
            validation_errors_ = True
            validation_errors.update({'p_iva': 'La partita iva non è valida'})

        if validation_errors_:
            return Response(validation_errors, status=status.HTTP_400_BAD_REQUEST)


        print(input_data)
        if request.user == restaurant.owner.user:
            # campi che possono essere modificati:
            # nome_attività, descrizione_attività, p_iva
            # numero di telefono del ristorante, city, address, cap

            for key in input_data:
                setattr(restaurant, key, input_data[key])

            restaurant.save()

            rest_data = ListRestaurantSerializer(restaurant)
            return Response(rest_data.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
