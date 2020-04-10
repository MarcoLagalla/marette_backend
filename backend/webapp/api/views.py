from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404

from .serializers import ListRestaurantSerializer, CreateRestaurantSerializer
from ..models import Restaurant
from ...account.models import Business
from ...account.permissions import IsBusiness


class ListRestaurantsAPIView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Restaurant.objects.all()
    serializer_class = ListRestaurantSerializer


class CreateRestaurantAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness]

    # only authenticated business users can create a new restaurant
    def post(self, request):
        user = get_object_or_404(Business, user=self.request.user)

        data = {}
        if user:
            serializer = CreateRestaurantSerializer(data=request.data, context={'business_user': user})
            if serializer.is_valid():
                restaurant = serializer.save()
                data['response'] = "successfully registered a new restaurant"
                data['id_restaurant'] = restaurant.id
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data['response'] = isinstance(user, Business)
        return Response(data, status=status.HTTP_403_FORBIDDEN)


class ShowRestaurantAPIView(APIView):
    pass
