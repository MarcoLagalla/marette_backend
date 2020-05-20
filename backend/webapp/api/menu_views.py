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

from ..models.models import Restaurant, Product
from backend.account.models import Business
from ..models.menu import Menu, MenuEntry

from .menus_serializers import MenuSerializer, WriteMenuSerializer, MenuEntrySerializer, WriteMenuEntrySerializer


class ListMenus(APIView):

    def get(self, request, id):
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        menus = Menu.objects.all().filter(restaurant=restaurant)
        serializer = MenuSerializer(menus, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AddMenu(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id):

        try:
            user = Business.objects.all().get(user=self.request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        if user:
            if user == restaurant.owner:
                serializer = WriteMenuSerializer(data=request.data)
                if serializer.is_valid():
                    menu = serializer.save(restaurant)
                    menu.save()
                    data = serializer.data
                    data.update({'id': menu.id, 'iva': menu.iva})
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_403_FORBIDDEN)


class DetailsMenu(APIView):
    permission_classes = [AllowAny]

    def get(self,request, id, m_id):
        restaurant_id = id
        menu_id = m_id

        try:
            restaurant = Restaurant.objects.all().get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            menu = Menu.objects.filter(restaurant=restaurant).get(id=menu_id)
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(menu)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteMenu(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, m_id):

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

                    # verifico che il menu sia un menu del mio ristorante
                    try:
                        menu = Menu.objects.all() \
                            .filter(restaurant=restaurant).get(id=m_id)
                        if menu:
                            menu.delete()
                            return Response(status=status.HTTP_200_OK)
                    except Menu.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class EditMenu(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, m_id):

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

                    # verifico che il menu sia un menu del mio ristorante
                    try:
                        menu = Menu.objects.all() \
                            .filter(restaurant=restaurant).get(id=m_id)
                        if menu:

                            serializer = WriteMenuSerializer(data=request.data)
                            if serializer.is_valid():
                                data = request.data
                                for key in data:
                                    setattr(menu, key, data[key])
                                menu.save()

                                return Response(status=status.HTTP_200_OK)
                            else:
                                return Response(status=status.HTTP_400_BAD_REQUEST)

                    except Menu.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MenuEntryAdd(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, m_id):
        try:
            user = Business.objects.all().get(user=self.request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            menu = Menu.objects.all().get(id=m_id)
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {}
        if user:
            if user == restaurant.owner:
                serializer = WriteMenuEntrySerializer(data=request.data)
                if serializer.is_valid():
                    menuentry = serializer.save(restaurant, menu)
                    menuentry.save()
                    data = serializer.data
                    data.update({'id': menuentry.id})
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_403_FORBIDDEN)


class MenuEntryDelete(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, m_id, me_id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            menu = Menu.objects.all().get(id=m_id)
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:

                    # verifico che il menu sia un menu del mio ristorante
                    try:
                        menu_entry = MenuEntry.objects.all() \
                            .filter(restaurant=restaurant).filter(menu=menu).get(id=me_id)
                        if menu_entry:
                            menu_entry.delete()
                            return Response(status=status.HTTP_200_OK)
                    except MenuEntry.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MenuEntryEdit(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, m_id, me_id):

        # verifico che l'utente sia il proprietario del ristorante
        try:
            token = Token.objects.all().get(user=request.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            menu = Menu.objects.all().get(id=m_id)
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            # utente loggato con token giusto
            # cerco un ristorante con l'id richiesto e verifico la paternità
            try:
                restaurant = Restaurant.objects.all().get(id=id)

                # verifico che sia proprietario del ristorante
                if restaurant.owner.user == request.user:

                    # verifico che il menu sia un menu del mio ristorante
                    try:
                        menu_entry = MenuEntry.objects.all() \
                            .filter(restaurant=restaurant).filter(menu=menu).get(id=me_id)
                        if menu_entry:

                            serializer = WriteMenuEntrySerializer(data=request.data)
                            if serializer.is_valid():
                                data = request.data
                                if 'products' in data:
                                    menu_entry.products.clear()
                                    for d in data['products']:
                                        try:
                                            product = Product.objects.all().filter(restaurant=restaurant).get(id=d)
                                            if product:
                                                menu_entry.products.add(d)
                                        except Product.DoesNotExist:
                                            pass
                                    del data['products']

                                for key in data:
                                    setattr(menu_entry, key, data[key])
                                menu_entry.save()

                                return Response(status=status.HTTP_200_OK)
                            else:
                                return Response(status=status.HTTP_400_BAD_REQUEST)

                    except MenuEntry.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)

            except Restaurant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class MenuEntryDetail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]
    def get(self, request, id, m_id, me_id):

        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            menu = Menu.objects.all().get(id=m_id)
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            menu_entry = MenuEntry.objects.all().filter(restaurant=restaurant).filter(menu=menu).get(id=me_id)
        except MenuEntry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MenuEntrySerializer(menu_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)
