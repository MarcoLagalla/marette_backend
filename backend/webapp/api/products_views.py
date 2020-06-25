import decimal

from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from django.db import transaction
from backend.account.permissions import IsBusiness, BusinessActivated
from rest_framework.authtoken.models import Token

from ..models.models import Restaurant, Product, ProductTag, ProductDiscount, FOOD_CATEGORY_CHOICES
from .products_serializers import ReadProductSerializer, WriteProductSerializer, ProductTagSerializer

import json


class ListProducts(APIView):

    def get(self, request, id):

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Non esiste ristorante con questo ID'},
                            status=status.HTTP_404_NOT_FOUND)

        # get all products for the restaurant
        products = Product.objects.filter(restaurant=restaurant)

        # if the restaurant does not have products
        if products.count() == 0:
            products_list = {}
            for val, category in FOOD_CATEGORY_CHOICES:
                products_list.update({category: []})
            return Response(products_list, status=status.HTTP_200_OK)

        products_list = {}
        # for each category
        for val, category in FOOD_CATEGORY_CHOICES:
            _cat_products = products.filter(category=category)
            _cat_products_data = ReadProductSerializer(_cat_products, many=True)
            products_list.update({category: _cat_products_data.data})

        return Response(products_list, status=status.HTTP_200_OK)


class AddProduct(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]
    parser_class = (MultiPartParser, FormParser, FileUploadParser)

    @transaction.atomic()
    def post(self, request, id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
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
                    try:
                        data = json.loads(request.data['data'])
                    except KeyError:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                    try:
                        image = request.FILES['image']
                        data.update({'image': image})
                    except Exception:
                        pass

                    serializer = WriteProductSerializer(data=data)
                    if serializer.is_valid():
                        ret_data = {}
                        product = serializer.save(restaurant)
                        ret_data = ReadProductSerializer(instance=product)
                        return Response(ret_data.data, status=status.HTTP_201_CREATED)
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
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, p_id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
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
                            product.delete()
                            return Response({'message': 'Prodotto eliminato correttamente'},
                                            status=status.HTTP_200_OK)
                    except Product.DoesNotExist:
                        return Response({'error': 'Prodotto non trovato'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'error': 'Non hai i Permessi necessari'}, status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response({'error': 'Ristorante non trovato'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UpdateProduct(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, p_id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
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

                            try:
                                data = json.loads(request.data['data'])
                            except KeyError:
                                return Response(status=status.HTTP_400_BAD_REQUEST)

                            try:
                                image = request.data['image']
                            except KeyError:
                                image = None

                            serializer = WriteProductSerializer(data=data)
                            if serializer.is_valid():
                                if 'tags' in data.keys():
                                    product.tags.clear()
                                    for tag in data['tags']:
                                        try:
                                            tag = ProductTag.objects.all().get(id=tag)
                                            if tag:
                                                product.tags.add(tag)
                                        except ProductTag.DoesNotExist:
                                            pass
                                    del data['tags']

                                try:
                                    data['price'] = decimal.Decimal(data['price'].replace(',', '.'))
                                except KeyError:
                                    pass

                                for key in data:
                                    setattr(product, key, data[key])

                                if image == '':
                                    product.image = None
                                elif image:
                                    product.image = image

                                product.save()
                                ret_data = ReadProductSerializer(instance=product)
                                return Response(ret_data.data, status=status.HTTP_200_OK)
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


class ProductDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, p_id):

        restaurant = get_object_or_404(Restaurant, id=id)
        try:
            product = Product.objects.all().filter(restaurant=restaurant).get(id=p_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReadProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListProductTags(ListAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
