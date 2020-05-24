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
from ..models.models import Restaurant
from .serializers import ListRestaurantSerializer, CreateRestaurantSerializer, RestaurantComponentsSerializer
from rest_framework.utils.urls import remove_query_param, replace_query_param
from django.core.paginator import Paginator


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
        page_number = request.query_params.get('page_number', 1)
        page_size = request.query_params.get('page_size', 10)

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
            'last': navigator.get_last_link()
        }

        data.update({'results': serializer.data})

        return Response(data, status=status.HTTP_200_OK)


class SearchRestaurantByCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queried_category = None
        restaurants = []

        try:
            queried_category = request.data['restaurant_category']
        except KeyError:
            pass

        if queried_category:
            restaurants = Restaurant.objects.filter(restaurant_category__iexact=queried_category).order_by('-id')
        else:
            return Response({'error': ["Non hai specificato alcuna categoria."]}, status.HTTP_400_BAD_REQUEST)

        if not restaurants:
            return Response({'error': ["Nessun Ristorante trovato nella categoria specificata."]},
                            status.HTTP_404_NOT_FOUND)

        # -----------------------------------------------------------
        page_number = request.query_params.get('page_number', 1)
        page_size = request.query_params.get('page_size', 10)

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
            'last': navigator.get_last_link()
        }

        data.update({'results': serializer.data})

        return Response(data, status=status.HTTP_200_OK)


class NavigationLinks:

    paginator = None
    page_number = None
    request = None

    def __init__(self, request, paginator, page_number):

        self.request = request
        self.paginator = paginator
        self.page_number = page_number

    def get_first_link(self):
        # page_number is the current page
        if int(self.page_number) == 1:
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, 'page_number', 1)

    def get_last_link(self):
        if int(self.page_number) == self.paginator.num_pages:
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, 'page_number', self.paginator.num_pages)

    def get_previous_link(self):
        url = self.request.build_absolute_uri()
        page = self.paginator.page(self.page_number)
        if page.has_previous():
            url = replace_query_param(url, 'page_number', page.previous_page_number())
        else:
            url = None
        return url

    def get_next_link(self):
        url = self.request.build_absolute_uri()
        page = self.paginator.page(self.page_number)
        if page.has_next():
            url = replace_query_param(url, 'page_number', page.next_page_number())
        else:
            url = None
        return url
