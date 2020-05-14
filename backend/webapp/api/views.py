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

        try:
            input_data = json.loads(request.data['data'])
        except json.JSONDecodeError as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = request.data['image']
        except Exception as err:
            image = None

        if request.user == restaurant.owner.user:
            # campi che possono essere modificati:
            # nome_attività, descrizione_attività, p_iva
            # numero di telefono del ristorante, city, address, cap

            serializer = CreateRestaurantSerializer(data=input_data)

            if serializer.is_valid():
                for key in input_data:
                    setattr(restaurant, key, input_data[key])

                if image == '':
                    restaurant.image = None
                elif image:
                    restaurant.image = image
                restaurant.save()

                rest_data = ListRestaurantSerializer(restaurant)
                return Response(rest_data.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class SearchRestaurantAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        queried_name = None
        queried_city = None
        restaurant = []

        try:
            queried_name = request.data['activity_name']
        except KeyError:
            pass
        try:
            queried_city = request.data['city']
        except KeyError:
            pass

        try:
            if queried_name and queried_city:
                restaurant = Restaurant.objects.filter(city__icontains=queried_city).filter(
                    activity_name__icontains=queried_name, activity_description__icontains=queried_name)

            elif queried_name:
                restaurant = Restaurant.objects.filter(activity_name__icontains=queried_name,
                                                             activity_description__icontains=queried_name)
            elif queried_city:
                restaurant = Restaurant.objects.filter(city__icontains=queried_city)
            else:

                return Response({'error': ["Non hai specificato alcun filtro."]},
                                status.HTTP_400_BAD_REQUEST)

            serializer = ListRestaurantSerializer(instance=restaurant, many=True)
            data = serializer.data

        except Restaurant.DoesNotExist:
            return Response({'error': ["Nessun Ristorante trovato che rispecchia i filtri specificati."]},
                            status.HTTP_404_NOT_FOUND)

        return Response(data, status.HTTP_200_OK)
