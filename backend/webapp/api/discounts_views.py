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

from ..models.models import Restaurant, Product, ProductTag, ProductDiscount
from .products_serializers import ProductDiscountSerializer


class ListDiscounts(ListAPIView):

    serializer_class = ProductDiscountSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['id']
        try:
            restaurant = Restaurant.objects.all().get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        discounts = ProductDiscount.objects.filter(restaurant=restaurant)
        if discounts.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return discounts


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
                        d = serializer.save()
                        d.restaurant = restaurant
                        d.save()
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
                    except Product.DoesNotExist:
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
                    except Product.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)