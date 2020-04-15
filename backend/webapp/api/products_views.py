from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from django.db import transaction
from backend.account.permissions import IsBusiness
from rest_framework.authtoken.models import Token

from ..models import Restaurant, Product, ProductTag, ProductDiscount
from .products_serializers import ReadProductSerializer, WriteProductSerializer

import json

class ListProducts(ListAPIView):
    serializer_class = ReadProductSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['id']
        return Product.objects.filter(restaurant_id=restaurant_id)


class AddProduct(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]
    parser_class = (MultiPartParser, FormParser, FileUploadParser)
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
                    # è il proprietario, può aggiungere un prodotto
                    image = request.data['image']
                    data = json.loads(request.data['data'])
                    data.update({'image': image})
                    serializer = WriteProductSerializer(data=data)
                    if serializer.is_valid():
                        ret_data = {}
                        product = serializer.save(restaurant)
                        ret_data.update(serializer.data)
                        ret_data.update({'image': product.image.url})
                        return Response(ret_data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteProduct(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, p_id):

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
                        product = Product.objects.all()\
                            .filter(restaurant=restaurant).get(id=p_id)
                        if product:
                            product.delete()
                            return Response(status=status.HTTP_200_OK)
                    except Product.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UpdateProduct(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, p_id):

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
                        product = Product.objects.all() \
                            .filter(restaurant=restaurant).get(id=p_id)
                        if product:

                            # fai update prodotto


                            return Response(status=status.HTTP_200_OK)
                    except Product.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)