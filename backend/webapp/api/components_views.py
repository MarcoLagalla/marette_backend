from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.db import transaction
from backend.account.permissions import IsBusiness
from rest_framework.authtoken.models import Token

from ..models.models import Restaurant
from ..models.components import MenuComponent, GalleriaComponent, EventiComponent, \
    VetrinaComponent, HomeComponent, ContattaciComponent


class ActivateComponent(APIView):
    permission_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, type):
        # controllo se gli oggetti esistono
        try:
            restaurant = Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Ristorante non trovato'}, status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user.auth_token.key != token:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user == restaurant.owner.user:
            # autorizzato
            panel = None
            type = type.lower()
            if type == 'home':
                try:
                    panel = HomeComponent.objects.all().get(restaurant=restaurant)
                except HomeComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'vetrina':
                try:
                    panel = VetrinaComponent.objects.all().get(restaurant=restaurant)
                except VetrinaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'menu':
                try:
                    panel = MenuComponent.objects.all().get(restaurant=restaurant)
                except MenuComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'galleria':
                try:
                    panel = GalleriaComponent.objects.all().get(restaurant=restaurant)
                except GalleriaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'eventi':
                try:
                    panel = EventiComponent.objects.all().get(restaurant=restaurant)
                except EventiComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'contattaci':
                try:
                    panel = ContattaciComponent.objects.all().get(restaurant=restaurant)
                except ContattaciComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if panel:
                panel.show = True
                panel.save()
                return Response({type: 'attivato'}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeactivateComponent(APIView):
    permission_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, type):
        # controllo se gli oggetti esistono
        try:
            restaurant = Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Ristorante non trovato'}, status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user.auth_token.key != token:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user == restaurant.owner.user:
            # autorizzato
            panel = None
            type = type.lower()
            if type == 'home':
                try:
                    panel = HomeComponent.objects.all().get(restaurant=restaurant)
                except HomeComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'vetrina':
                try:
                    panel = VetrinaComponent.objects.all().get(restaurant=restaurant)
                except VetrinaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'menu':
                try:
                    panel = MenuComponent.objects.all().get(restaurant=restaurant)
                except MenuComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'galleria':
                try:
                    panel = GalleriaComponent.objects.all().get(restaurant=restaurant)
                except GalleriaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'eventi':
                try:
                    panel = EventiComponent.objects.all().get(restaurant=restaurant)
                except EventiComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'contattaci':
                try:
                    panel = ContattaciComponent.objects.all().get(restaurant=restaurant)
                except ContattaciComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if panel:
                panel.show = False
                panel.save()
                return Response({type: 'disattivato'}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
