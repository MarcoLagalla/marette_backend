import django
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from ..models.models import Restaurant, FasciaOraria, GiornoApertura, OrarioApertura
from .serializers import ListRestaurantSerializer, CreateRestaurantSerializer, RestaurantComponentsSerializer
from rest_framework.utils.urls import remove_query_param, replace_query_param
from django.core.paginator import Paginator

from .serializers import ListRestaurantSerializer
from ..models.models import Restaurant
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

        queried_aperto_ora = None
        queried_aperto_oggi = None
        fascie_orarie = None

        try:
            queried_aperto_ora = request.data['aperto_ora']
        except KeyError:
            pass

        try:
            queried_aperto_oggi = request.data['aperto_oggi']
        except KeyError:
            pass

        aperto_ora = []
        aperto_oggi = []

        if queried_aperto_ora or queried_aperto_oggi:
            today = datetime.datetime.now().weekday()
            current_hour = datetime.datetime.now().replace(tzinfo=utc).strftime('%H')
            current_minutes = datetime.datetime.now().replace(tzinfo=utc).strftime('%M')
            current_time = int(current_hour) * 60 + int(current_minutes)
            # print(current_hour, current_minutes)

            try:
                fascie_orarie = FasciaOraria.objects.all().filter(giorno__day__exact=DAYS[today][0])
                # print("aperto oggi", fascie_orarie)
            except IndexError:
                pass

            if fascie_orarie:
                for fascia_oraria in fascie_orarie:
                    aperto_oggi.append([fascia_oraria.restaurant, fascia_oraria.giorno.day, fascia_oraria.start, fascia_oraria.end])
                   # print(aperto.restaurant, aperto.giorno.day, aperto.start, aperto.end)
                    start_hour = fascia_oraria.start[:2]
                    start_minute = fascia_oraria.start[3:]
                    end_hour = fascia_oraria.end[:2]
                    end_minute = fascia_oraria.end[3:]
                    start_time = int(start_hour) * 60 + int(start_minute)
                    end_time = int(end_hour) * 60 + int(end_minute)

                    # check if aperto adesso
                    if start_time <= current_time <= end_time:
                        print("APERTO !")
                        aperto_ora.append([fascia_oraria.restaurant, fascia_oraria.giorno.day, fascia_oraria.start, fascia_oraria.end])

                    # check if not aperto adesso ma apre tra + - 30min
                    timedelta_ = 1 * 60

        print("aperto_ora", aperto_ora)    # DEBUG
        print("aperto_oggi", aperto_oggi)  # DEBUG

        if queried_aperto_ora:
            open_restaurant = len(aperto_ora)
            if open_restaurant:
                for i, restaurant in enumerate(aperto_ora):
                    print("YES", restaurant)


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





