from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from django.db import transaction
from backend.account.permissions import IsBusiness
from rest_framework.authtoken.models import Token

from ..models.models import Restaurant
from ..models.menu import Menu, MenuEntry

from .menus_serializers import MenuSerializer, MenuEntrySerializer


class ListMenus(ListAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['id']
        try:
            restaurant = Restaurant.objects.all().get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        menus = Menu.objects.filter(restaurant=restaurant)
        if menus.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return menus


class AddMenu(APIView):
    pass


class DetailsMenu(APIView):
    pass


class EditMenu(APIView):
    pass


class DeleteMenu(APIView):
    pass
