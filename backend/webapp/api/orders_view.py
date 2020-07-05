from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .orders_serializers import OrderSerializer, ReadOrderSerializer
from ...account.models import Customer
from ...account.views import send_order_email
from ..models.orders import Order


class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    @transaction.atomic()
    def post(self, request):
        try:
            user = request.data['user']
            user = Customer.objects.all().get(id=user)
        except User.DoesNotExist:
            return Response({'error': 'user'}, status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=user.user).key
        except Token.DoesNotExist:
            return Response({'error': 'token'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.auth_token.key == token:
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():
                order = serializer.save()
                send_order_email(order.restaurant.owner, order)
                ret_data = ReadOrderSerializer(instance=order)
                return Response(ret_data.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, id):

        try:
            order = Order.objects.all().get(id=id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            if request.user != order.user.user:
                if request.user != order.restaurant.owner.user.user:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ReadOrderSerializer(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)