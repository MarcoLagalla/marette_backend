from django.db import transaction
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from backend.account.permissions import IsBusiness, BusinessActivated
from backend.webapp.models.models import Restaurant
from backend.webapp.api.opening_hours_serializers import  *


class CreateOpening(APIView):

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

        if token == request.user.auth_token.key:
            # proprietario

            try:

                orario = OrarioApertura.objects.all().get(restaurant=restaurant)
                return Response(status=status.HTTP_204_NO_CONTENT)

            except OrarioApertura.DoesNotExist:

                orario = OrarioApertura.objects.create(restaurant=restaurant)
                orario.save()

                data = {'status': 'Creato',
                        'id': orario.id}
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateOpeningDay(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id):
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        if token == request.user.auth_token.key:

            serializer = GiornoAperturaSerializer(data=request.data)
            if serializer.is_valid():

                try:
                    d = GiornoApertura.objects.filter(restaurant=restaurant).\
                        get(day__iexact=serializer.validated_data['day'])

                    return Response(status=status.HTTP_204_NO_CONTENT)
                except GiornoApertura.DoesNotExist:
                    day = serializer.save()
                    data = {'status': 'Giorno apertura creato',
                            'id': day.id}
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreateFasciaOraria(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, d_id):
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            day = GiornoApertura.objects.filter(restaurant=restaurant).get(id=d_id)
        except GiornoApertura.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:
            serializer = FasciaOrariaSerializer(data=request.data)
            if serializer.is_valid():
                fascia = serializer.save(day)
                ser = FasciaOrariaSerializer(instance=fascia)
                data = {}
                data.update(ser.data)
                data.update({'id': fascia.id})
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteFasciaOraria(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, f_id):
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:

            try:
                fascia = FasciaOraria.objects.filter(restaurant=restaurant).get(id=f_id)
            except FasciaOraria.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            fascia.delete()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteOpeningDay(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id, d_id):
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:

            try:
                day = GiornoApertura.objects.filter(restaurant=restaurant).get(id=d_id)
            except GiornoApertura.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            day.delete()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteOpening(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness, BusinessActivated]

    @transaction.atomic()
    def post(self, request, id):
        try:
            restaurant = Restaurant.objects.all().get(id=id)
        except Restaurant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if token == request.user.auth_token.key:

            try:
                opening = OrarioApertura.objects.all().get(restaurant=restaurant)
            except OrarioApertura.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            opening.delete()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
