import json

import django
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import transaction
from localflavor.it.util import vat_number_validation
from rest_framework import status, serializers
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import ListRestaurantSerializer, CreateRestaurantSerializer, RestaurantComponentsSerializer, \
    VoteRestaurantSerializer, CategorySerializer
from ..models.components import RestaurantComponents
from ..models.models import Restaurant, CustomerVote, Category
from ...account.models import Business, Customer
from ...account.permissions import IsBusiness, BusinessActivated, IsCustomer, CustomerActivated
from ...utils import NavigationLinks


class ListRestaurantsAPIView(ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        restaurants = Restaurant.objects.all()

        if not restaurants:
            return Response({'error': ["Nessun Ristorante trovato nella categoria specificata."]}, status.HTTP_404_NOT_FOUND)

        # -----------------------------------------------------------
        page_number = request.GET.get('page_number', 1)
        page_size = request.GET.get('page_size', 10)

        try:
            paginator = Paginator(restaurants.distinct().order_by('-id'), page_size)
            page = paginator.page(page_number)
        except EmptyPage:
            page_number = 1
            page = paginator.page(page_number)


        serializer = ListRestaurantSerializer(page, many=True, context={'request': request})
        # -----------------------------------------------------------

        navigator = NavigationLinks(self.request, paginator, page_number)

        data = {
            'first': navigator.get_first_link(),
            'previous': navigator.get_previous_link(),
            'next': navigator.get_next_link(),
            'last': navigator.get_last_link(),
            'page_size': page_size,
            'page_number': page_number
        }

        data.update({'results': serializer.data})

        return Response(data, status=status.HTTP_200_OK)


class CreateRestaurantAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

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
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

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

            try:
                p_iva = input_data['p_iva']
                if not vat_number_validation(p_iva):
                    raise serializers.ValidationError({'p_iva': 'La partita iva non è valida'})
            except ValueError:
                raise serializers.ValidationError({'p_iva': 'La partita iva non è valida'})

            serializer = CreateRestaurantSerializer(data=input_data)

            if serializer.is_valid():
                try:
                    categories = input_data['restaurant_category']
                    del input_data['restaurant_category']
                    restaurant.restaurant_category.clear()
                    for cat in categories:
                        c = Category.objects.all().get(id=cat)
                        restaurant.restaurant_category.add(c)
                except KeyError:
                    pass

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


class VoteRestaurantAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer, CustomerActivated]

    @transaction.atomic()
    def post(self, request, id):
        try:
            customer = Customer.objects.all().get(user=self.request.user)
        except Customer.DoesNotExist:
            return Response({'error': ["Utente non trovato."]}, status=status.HTTP_404_NOT_FOUND)

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': ["Ristorante non trovato."]}, status.HTTP_404_NOT_FOUND)

        if restaurant and customer:
            serializer = VoteRestaurantSerializer(data=request.data, many=False)
            if serializer.is_valid():
                new_vote = serializer.validated_data['vote']
                rank = 0
                has_vote = None

                try:
                    all_past_vote = CustomerVote.objects.all().filter(restaurant__exact=restaurant)
                    has_vote = all_past_vote.get(customer__exact=customer)
                except CustomerVote.DoesNotExist:
                    pass

                try:
                    if all_past_vote:
                        sum_vote = sum([cust_vote.vote for cust_vote in all_past_vote])
                        rank = round((sum_vote + new_vote) / (len(all_past_vote)+1))
                    else:
                        rank = serializer.validated_data['vote']
                except ZeroDivisionError:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                if has_vote:
                    return Response({'error': ["Hai già votato questo ristorante."]},
                                    status=status.HTTP_401_UNAUTHORIZED)
                else:
                    serializer.save(customer, restaurant, rank)
                    return Response({'success': ["Grazie per aver votato questo ristorante."]}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': ["Voto non registrato."]}, status=status.HTTP_401_UNAUTHORIZED)


class RestaurantCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category_list = Category.objects.all()
        serializer = CategorySerializer(instance=category_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteRestaurantAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic
    def post(self, request, id):

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.auth_token.key == token:

            confirm = request.data.get('confirm', None)

            if not confirm:
                return Response({'error': 'Codice conferma mancante.'})
            else:
                if confirm == restaurant.url:
                    # delete restaurant
                    restaurant.delete()
            return Response({'status': 'Ristorante cancellato.'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
