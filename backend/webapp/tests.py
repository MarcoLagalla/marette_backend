import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
# from .api.serializers import CustomerSerializer, BusinessSerializer
from ..account.models import Customer, Business
from django.contrib.auth.hashers import make_password


class RestaurantRegistrationTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app',
                                          password=make_password('12345'))
        buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}
        base_business = Business.objects.create(user=base_user_b, **buss_user_data)


    # def test_can_create_business_user(self):
    #     response = self.client.post(reverse('account:register_business'), self.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_business_can_create_restaurant(self):  # 200 o 201
        #create business or use the base one
        user = User.objects.get(username='mikeB')
        token, created = Token.objects.get_or_create(user=user)
        print("LOGOUT TOKEN = ", token.key)


    def test_no_business_can_create_restaurant(self):   #404 o 403
        pass

    def test_can_list_restaurant(self):
        pass
        # response = self.client.get(reverse('webapp:list_restaurants'))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        #add check con il ristorante creato




    def test_can_show_restaurant(self):
        response = self.client.get('api/v1/restaurant/' + str(1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   #change here after have created a restaurant

