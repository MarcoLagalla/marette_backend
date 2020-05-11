from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from django.db import transaction
from backend.account.permissions import IsBusiness
from rest_framework.authtoken.models import Token

from ..models.models import Restaurant, Product, ProductTag, ProductDiscount, RestaurantDiscount
from .products_serializers import ProductDiscountSerializer
from .serializers import RestaurantDiscountSerializer


class ListDiscounts(APIView):

    def get(self, request, id):
        restaurant_id = id
        try:
            restaurant = Restaurant.objects.all().get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        discounts = ProductDiscount.objects.filter(restaurant=restaurant)

        serializer = ProductDiscountSerializer(discounts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailsDiscounts(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, d_id):
        try:
            discount = ProductDiscount.objects.all().filter(restaurant_id=id).get(id=d_id)
        except ProductDiscount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDiscountSerializer(discount)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddDiscounts(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness]

    @transaction.atomic()
    def post(self, request, id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:
                    # è il proprietario, può aggiungere un discount

                    serializer = ProductDiscountSerializer(data=request.data)
                    if serializer.is_valid():
                        d = serializer.save(restaurant)
                        return Response(serializer.validated_data,
                                        status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors,
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class EditDiscounts(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, d_id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:

                    # verifico che il discount prod sia del mio ristorante
                    try:
                        discount = ProductDiscount.objects.all() \
                            .filter(restaurant=restaurant).get(id=d_id)
                        if discount:
                            serializer = ProductDiscountSerializer(data=request.data)
                            if serializer.is_valid():
                                for key in serializer.validated_data:
                                    setattr(discount, key, serializer.validated_data[key])
                                discount.restaurant = restaurant
                                discount.save()
                                return Response(status=status.HTTP_200_OK)
                            else:
                                return Response(serializer.errors,
                                                status=status.HTTP_400_BAD_REQUEST)
                    except ProductDiscount.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteDiscounts(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, d_id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:

                    # verifico che il discount prod sia del mio ristorante
                    try:
                        discount = ProductDiscount.objects.all() \
                            .filter(restaurant=restaurant).get(id=d_id)
                        if discount:
                            discount.delete()
                            return Response(status=status.HTTP_200_OK)
                    except ProductDiscount.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AddRestaurantDiscounts(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness]

    @transaction.atomic()
    def post(self, request, id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:
                    # creo il discount
                    serializer = RestaurantDiscountSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save(restaurant)
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors,
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListRestaurantDiscounts(APIView):

    def get(self, request, id):

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            discounts = RestaurantDiscount.objects.all().filter(restaurant=restaurant)
        except RestaurantDiscount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RestaurantDiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailsRestaurantDiscounts(APIView):

    def get(self, request, id, d_id):

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            discounts = RestaurantDiscount.objects.all().filter(restaurant=restaurant).get(id=d_id)
        except RestaurantDiscount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RestaurantDiscountSerializer(discounts)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditRestaurantDiscounts(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness]

    @transaction.atomic()
    def post(self, request, id, d_id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:
                    try:
                        discount = ProductDiscount.objects.all() \
                            .filter(restaurant=restaurant).get(id=d_id)
                        if discount:
                            serializer = RestaurantDiscountSerializer(data=request.data)
                            if serializer.is_valid():
                                for key in serializer.validated_data:
                                    setattr(discount, key, serializer.validated_data[key])

                                discount.restaurant = restaurant
                                discount.save()
                                return Response(status=status.HTTP_200_OK)
                            else:
                                return Response(serializer.errors,
                                                status=status.HTTP_400_BAD_REQUEST)
                    except ProductDiscount.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteRestaurantDiscounts(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness]

    @transaction.atomic()
    def post(self, request, id, d_id):

        # verifico che l'utente sia il proprietario del ristorante

        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:

                    # verifico che il prodotto sia un prodotto del mio ristorante
                    try:

                        discount = RestaurantDiscount.objects.all() \
                            .filter(restaurant=restaurant).get(id=d_id)

                        if discount:
                            discount.delete()
                            return Response(status=status.HTTP_200_OK)

                    except RestaurantDiscount.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
