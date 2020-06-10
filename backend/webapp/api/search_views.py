import json
import django
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from ..models.models import Restaurant, FasciaOraria, GiornoApertura
from .serializers import ListRestaurantSerializer, CreateRestaurantSerializer, RestaurantComponentsSerializer
from rest_framework.utils.urls import remove_query_param, replace_query_param
from django.core.paginator import Paginator
from ...utils import NavigationLinks
import datetime
from django.utils.timezone import utc
from backend.webapp.declarations import DAYS


class SearchRestaurantAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queried_name = None
        queried_city = None
        restaurants = []

        try:
            queried_name = request.data['query']
        except KeyError:
            pass
        try:
            queried_city = request.data['city']
        except KeyError:
            pass

        if queried_name and queried_city:
            activity_name_queryset = Restaurant.objects.filter(city__icontains=queried_city).filter(
                activity_name__icontains=queried_name).order_by('-id')
            activity_description_queryset = Restaurant.objects.filter(city__icontains=queried_city).filter(activity_description__icontains=queried_name).order_by('-id')
            restaurants = activity_name_queryset | activity_description_queryset

        elif queried_name:
            activity_name_queryset = Restaurant.objects.filter(activity_name__icontains=queried_name).order_by('-id')
            activity_description_queryset = Restaurant.objects.filter(activity_description__icontains=queried_name).order_by('-id')
            restaurants = activity_name_queryset | activity_description_queryset

        elif queried_city:
            restaurants = Restaurant.objects.filter(city__icontains=queried_city).order_by('-id')
        else:
            return Response({'error': ["Non hai specificato alcun filtro."]}, status.HTTP_400_BAD_REQUEST)

        if not restaurants:
            return Response({'error': ["Nessun Ristorante trovato che rispecchia i filtri specificati."]},
                            status.HTTP_404_NOT_FOUND)

        # -----------------------------------------------------------
        page_number = request.data.get('page_number', 1)
        page_size = request.data.get('page_size', 10)

        try:
            paginator = Paginator(restaurants.distinct(), page_size)
            page = paginator.page(page_number)
        except django.core.paginator.EmptyPage:
            page = paginator.page(1)

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


class SearchRestaurantByQueryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queried_name = None
        queried_city = None
        queried_category = None
        queryset = []

        try:
            queried_name = request.data['restaurant_name']
        except KeyError:
            pass

        try:
            queried_city = request.data['restaurant_city']
        except KeyError:
            pass

        try:
            queried_category = request.data['restaurant_category']
        except KeyError:
            pass

        try:
            aperto_ora = request.data['aperto_ora']
        except KeyError:
            pass

        if aperto_ora:

            # giorno apertura check
            try:
                today = datetime.datetime.now().weekday()
                aperti_oggi = GiornoApertura.objects.all().filter(day__exact=DAYS[today][0])
                print(aperti_oggi)
                #fasce_orarie = FasciaOraria.objects.all().filter(giorno__exact=today)
                #print(fasce_orarie)
            except IndexError:
                pass

            if aperti_oggi:
                for aperto in aperti_oggi:
                    print(aperto.day)
                    print(aperto.fasce)


            # ora recupera la fascia oraria
            # try:
            #     today = datetime.datetime.now().weekday()
            #     #print(type(today), today)
            #
            #     fasce_orarie = FasciaOraria.objects.all().filter(giorno__exact=today)
            #     #print(fasce_orarie)
            # except IndexError:
            #     pass
            #
            # if fasce_orarie:
            #     for fascia in fasce_orarie:
            #         print(fascia.giorno.day, fascia.start, fascia.end)




       #     print("test", datetime.datetime.now().strftime("%A"))
            # print(datetime.datetime.now().weekday())
            #print(DAYS[datetime.datetime.now().weekday()])

            # now = datetime.datetime.utcnow().replace(tzinfo=utc).strftime('%D %H:%M:%S')
            # print(now)




        if queried_name:
            name_query = Restaurant.objects.filter(activity_name__icontains=queried_name).order_by('-id')
            description_query = Restaurant.objects.filter(activity_description__icontains=queried_name).order_by('-id')
            queryset.append(name_query | description_query)

        if queried_city:
            city_query = Restaurant.objects.filter(city__iexact=queried_city).order_by('-id')
            queryset.append(city_query)

        if queried_category:
            category_query = Restaurant.objects.filter(restaurant_category__category_name__iexact=queried_category).order_by('-id')
            queryset.append(category_query)

        try:
            results_query = None

            if queryset:
                results_query = queryset[0]
                for query in queryset:
                    results_query = results_query & query

            if results_query:
                # -----------------------------------------------------------
                page_number = request.data.get('page_number', 1)
                page_size = request.data.get('page_size',  10)

                try:
                    paginator = Paginator(results_query.distinct(), page_size)
                    page = paginator.page(page_number)
                except django.core.paginator.EmptyPage:
                    page = paginator.page(1)

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

        except KeyError:
            return Response({'error': ["Nessun Ristorante trovato secondo i filtri specificati."]},
                            status.HTTP_404_NOT_FOUND)

        return Response({'error': ["Nessun Ristorante trovato secondo i filtri specificati."]},
                        status.HTTP_404_NOT_FOUND)





