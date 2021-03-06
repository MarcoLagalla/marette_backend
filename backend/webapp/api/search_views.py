from functools import reduce

import django
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ListRestaurantSerializer
from ..models.models import Restaurant
from ...utils import NavigationLinks


class SearchRestaurantAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queried_name = None
        queried_city = None
        restaurants = []

        try:
            queried_name = request.GET.get('query', '')
        except KeyError:
            pass
        try:
            queried_city = request.GET.get('city', '')
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
        page_number = request.GET.get('page_number', 1)
        page_size = request.GET.get('page_size', 10)

        try:
            paginator = Paginator(restaurants.distinct(), page_size)
            page = paginator.page(page_number)
        except django.core.paginator.EmptyPage:
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


class SearchRestaurantByQueryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queried_name = None
        queried_city = None
        queried_category = None

        queried_aperto_ora = None
        queried_aperto_oggi = None
        fascie_orarie = None
        queryset = []
        aperto_ora = []
        aperto_oggi = []

        # valid_params = ['page_size', 'page_number', 'query', 'city', 'restaurant_category', 'aperto_ora', 'aperto_oggi']
        # for param in request.GET:
        #     if param not in valid_params:
        #         return Response({'error': f'Filtro {param} non valido.'},
        #                         status=status.HTTP_400_BAD_REQUEST)

        try:
            queried_name = request.GET.get('query', None)
        except KeyError:
            pass

        try:
            queried_city = request.GET.get('city', None)
        except KeyError:
            pass

        try:
            queried_category = request.GET.get('restaurant_category', None)
        except KeyError:
            pass

        try:
            queried_aperto_ora = request.GET.get('aperto_ora', None)
        except KeyError:
            pass

        try:
            queried_aperto_oggi = request.GET.get('aperto_oggi', None)
        except KeyError:
            pass

        # if queried_aperto_ora or queried_aperto_oggi:
        #     today = datetime.datetime.now().weekday()
        #     current_hour = datetime.datetime.now().replace(tzinfo=utc).strftime('%H')
        #     current_minutes = datetime.datetime.now().replace(tzinfo=utc).strftime('%M')
        #     current_time = int(current_hour) * 60 + int(current_minutes)
        #
        #     try:
        #         fascie_orarie = FasciaOraria.objects.all().filter(giorno__day__exact=DAYS[today][0])
        #     except IndexError:
        #         pass
        #
        #     if fascie_orarie:
        #         for fascia_oraria in fascie_orarie:
        #             aperto_oggi.append([fascia_oraria.restaurant, fascia_oraria.giorno.day, fascia_oraria.start, fascia_oraria.end])
        #             start_hour = fascia_oraria.start[:2]
        #             start_minute = fascia_oraria.start[3:]
        #             end_hour = fascia_oraria.end[:2]
        #             end_minute = fascia_oraria.end[3:]
        #             start_time = int(start_hour) * 60 + int(start_minute)
        #             end_time = int(end_hour) * 60 + int(end_minute)
        #
        #             # check if aperto adesso
        #             if start_time <= current_time <= end_time:
        #                 aperto_ora.append(fascia_oraria.restaurant)
        #
        #             # check if not aperto adesso ma apre tra + - 30min
        #             timedelta_ = 1 * 60
        #             # TODO

        # if queried_aperto_ora:
        #     open_restaurant = len(aperto_ora)
        #     if open_restaurant:
        #         for i, restaurant in enumerate(aperto_ora):
        #             open_restaurant_query = Restaurant.objects.filter(activity_name__iexact=restaurant).order_by('-id')
        #             queryset.append(open_restaurant_query)
        #     else:
        #         return Response({'error': ["Nessun Ristorante trovato."]},
        #                         status.HTTP_404_NOT_FOUND)

        if queried_aperto_ora:
            restaurants = Restaurant.objects.all()
            wanted_list = []
            for rest in restaurants:
                if rest.is_open():
                    # rest aperto
                    wanted_list.append(rest.id)
            queryset.append(Restaurant.objects.filter(pk__in=wanted_list))

        if queried_name:
            queried_name_list = queried_name.split(' ')
            name_query = Restaurant.objects.filter(reduce(lambda x, y: x | y, [Q(activity_name__icontains=word) for word
                                                                               in queried_name_list])).order_by('-id')
            description_query = Restaurant.objects.filter(activity_description__icontains=queried_name).order_by('-id')

            if not queried_city:
                city_query = Restaurant.objects.filter(city__icontains=queried_name).order_by('-id')
                queryset.append(name_query | description_query | city_query)
            else:
                queryset.append(name_query | description_query)

        if queried_city:
            city_query = Restaurant.objects.filter(city__iexact=queried_city).order_by('-id')
            queryset.append(city_query)

        if queried_category:
            category_query = Restaurant.objects.filter(restaurant_category__category_name__iexact=queried_category).order_by('-id')
            queryset.append(category_query)

        results_query = None

        if queryset:
            results_query = queryset[0]
            for query in queryset:
                results_query = results_query & query

        else:
            results_query = Restaurant.objects.all().order_by('-id')

        if results_query:
            # -----------------------------------------------------------
            page_number = request.GET.get('page_number', 1)
            page_size = request.GET.get('page_size', 10)

            try:
                paginator = Paginator(results_query.distinct().order_by('-id'), page_size)
                page = paginator.page(page_number)
            except django.core.paginator.EmptyPage:
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
        else:
            return Response({'error': ["Nessun Ristorante trovato."]},
                            status.HTTP_404_NOT_FOUND)


class AutoComplete(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request):

        restaurants = Restaurant.objects.all()

        values = restaurants.values('city').distinct().order_by('city').values_list('city')
        cities_list = []
        for val in values:
            cities_list.append(str(val[0]).capitalize())

        data = {'cities': cities_list}

        names = restaurants.values('activity_name').order_by('activity_name').values_list('activity_name')
        names_list = []
        for val in names:
            names_list.append(val[0])

        data.update({'names': names_list})
        return Response(data, status=status.HTTP_200_OK)
