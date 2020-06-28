import json
from django.http import QueryDict
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
# from .api.serializers import CustomerSerializer, BusinessSerializer
from ..account.models import Customer, Business
from django.contrib.auth.hashers import make_password
from .models.models import Restaurant, Category
from django.test import Client


class RestaurantTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='1234')

        #base customer
        base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app',
                                        password=make_password('12345'))
        cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        base_customer = Customer.objects.create(user=base_user, **cust_user_data)

        #base_business
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}
        self.base_business = Business.objects.create(user=self.base_user_b, **buss_user_data)
        self.base_business.email_activated = True
        self.base_business_token = Token.objects.create(user=self.base_user_b)
       # print(self.base_business_token)


        #base_restaurant
        rest_base_data = {"activity_name": "Pizzeria Ancora", "activity_description": "Tutto buonissimo",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100",
                          "p_iva": "IT01766920761", "restaurant_number": "3456765789"}

        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")
        base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        base_restaurant.restaurant_category.set([1, 2])
        base_restaurant.set_url()

        self.datastr = '{\n\t"activity_name": "Pizzeria Ancora", \n\t"activity_description": "Tutto buonissimo", ' \
                       '\n\t"p_iva": "04113940409", \n\t"restaurant_number": "3456765789", ' \
                       '\n\t"city": "pavia", \n\t"address": "marconi nuova", \n\t"n_civ": "25", \n\t"cap": "27100", ' \
                       '\n\t"restaurant_category": ""}'


    def test_business_can_create_restaurant(self):  # 200 o 201

        print(self.base_business.email_activated)

        # # resend acytivation email
        # self.client.login(username='mikeB', password='12345')
       # self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        # response = self.client.post(reverse('account:resend_token', kwargs={'id': self.base_user_b.id}))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print("ACT: ", self.base_business.activation_token)

        self.client.force_login(self.base_user_b)

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr})

        #self.client.login(username='mikeB', password='12345')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        # # session = self.client.session
        # # session['documents_to_share_ids'] = [1]
        # # session.save()
        #
        # # session = self.client.session
        # # session.update({
        # #     "expire_date": '2010-12-05',
        # #     "session_key": 'my_session_key',
        # # })
        # # session.save()
        #
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_no_business_can_create_restaurant(self):   #404
        pass
    #     user = User.objects.get(username='mike')
    #     token, created = Token.objects.get_or_create(user=user)
    #
    #     query_dict = QueryDict('', mutable=True)
    #     query_dict.update({'data': self.datastr})
    #
    #     self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
    #     response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_list_restaurant(self):
        response = self.client.get(reverse('webapp:list_restaurants'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_show_restaurant(self):
        restaurant = Restaurant.objects.get(activity_name="Pizzeria Ancora")
        response = self.client.get(reverse('webapp:show_restaurant', kwargs={'id': restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
   #     self.assertEqual(response.data['owner'], "mikeB")
        self.assertEqual(response.data['activity_name'], "Pizzeria Ancora")
        self.assertEqual(response.data['p_iva'], "IT01766920761")



