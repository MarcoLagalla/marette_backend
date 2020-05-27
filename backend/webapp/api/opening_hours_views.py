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
            serializer = OpeningSerializer(data=request.data)
            if serializer.is_valid():
                #creo
                data = {'status': 'Orario creato.'}
                orario = serializer.save()
                data.update({'id': orario.id})
                return Restaurant(data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


