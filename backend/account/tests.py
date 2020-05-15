import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
from .api.serializers import CustomerSerializer, BusinessSerializer
from .models import Customer, Business
from rest_framework.authtoken.models import Token
from django.test import Client
from django.contrib.auth.hashers import make_password


class CustomerRegistrationTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """ Static method for the access of a base customer user need to perform tests. """
        superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app', password=make_password('12345'))
        cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        base_customer = Customer.objects.create(user=base_user, **cust_user_data)

        test_creaz_cust = {'username': 'mike_test', 'first_name': 'Mike2', 'last_name': 'Tyson2',
                           'email': 'test2@test.app', 'password': '12345', 'password2': '12345',
                                'birth_date': '1994-04-20', 'phone': '3458926931'}




    # def setUp(self):
    #     self.superuser = User.objects.create_superuser(username='admin',
    #                                                    email='admin@gmail.com',
    #                                                    password='1234')
    #
    #     self.data = {'username': 'mike_test', 'first_name': 'Mike2', 'last_name': 'Tyson2',
    #                  'email': 'test2@test.app', 'password': '12345', 'password2': '12345',
    #                  "birth_date": "1994-04-20", "phone": "3458926931"}

    def test_can_create_user(self):
        pass
        #self.test_can_logout_user()
        #
        # self.data = {"username": "mike_test", "first_name": "Mike2", "last_name": "Tyson2",
        #                    "email": "test2@test.app", 'password': "12345", "password2": "12345",
        #                         "birth_date": "1994-04-20", "phone": "3458926931"}
        #
        # self.json_data = json.dumps(self.data)
        #
        # response = self.client.post(reverse('account:register_customer'), self.data, content_type="application/json")
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #
        # self.assertEqual(len(response.data), 5)

       # # response = self.client.post(reverse('account:register_customer'), json_data, content_type="application/json")
       #  response = self.client.post(reverse('account:register_customer'), test_creaz_cust)
       #  self.assertEqual(response.status_code, status.HTTP_201_CREATED)            # TODO ADD check output and not only the status code !
       # #  self.assertEqual(len(response.data), 5)
       # # # self.assertEqual(response.data['username'], self.data['username'])
       # #  self.assertTrue(response.data['token'], response.data['id'])

      #  self.user = User.objects.get_or_create(username='mike')[0]




    def test_can_logout_user(self):
        user = User.objects.get(username='mike')
        token, created = Token.objects.get_or_create(user=user)
        print("LOGOUT TOKEN = ", token.key)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_login_user(self):
        json_data = json.dumps({"email": 'test@test.app', "password": "12345"})
        response = self.client.post(reverse('account:login'), json_data, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
       # print(response.data['token'])
        self.assertTrue(response.data['token'])
        self.assertEqual(len(response.data), 2)

    def test_admin_list_user(self):
        superuser = User.objects.get_or_create(username='admin')[0]
        self.client.force_login(superuser)
        response = self.client.get(reverse('account:list'))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_no_admin_list_user(self):
        base_customer = User.objects.get(id='2')  # or username='mike'
        self.client.force_login(base_customer)
        response = self.client.get(reverse('account:list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.content, b'{"detail":"Non hai l\'autorizzazione per eseguire questa azione."}')

    def test_user_profile(self):
        pass
       #  json_data = json.dumps({"email": 'test@test.app', "password": "12345"})
       #  response = self.client.post(reverse('account:login'), json_data, content_type="application/json")
       #
       # # self.assertEqual(response.status_code, status.HTTP_200_OK)
       #  print("TEST USER PROF", response.data['token'])
       #  print("ID=", response.data['id'])
       #
       #  self.client = Client(HTTP_AUTHORIZATION='Token ' + response.data['token'])
       #  response = self.client.get('api/v1/account/profile/2')
       #  self.assertEqual(response.status_code, status.HTTP_200_OK)



        # user = User.objects.get(username='mike') #id='2')
        #     #User.objects.get_or_create(username='mike')[0]
        # #print(user, user.id, user.phone)
        # token, created = Token.objects.get(user=user) #.get_or_create(user=user)
        # print("TOKEN = ", token.key)

        #
        # json_data = json.dumps({"email": 'test@test.app', "password": "12345"})
        # response = self.client.post(reverse('account:login'), json_data, content_type="application/json")
        # print(response.data['token'])
        #
        # self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        # response = self.client.post('api/v1/account/profile/2')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # json_data = json.dumps({"email": 'test@test.app', "password": "12345"})
        # response = self.client.post(reverse('account:login'), json_data, content_type="application/json")
        # print(response.data['token'])
        #
        # self.client = Client(HTTP_AUTHORIZATION='Token ' + response.data['token'])
        # response = self.client.get('api/v1/account/profile/2' )
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # self.client.force_login(user)
        #
        # # user = self.superuser
        # # self.client.force_login(user)
        # response = self.client.get('api/v1/account/profile/' + str(user.id))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_update_user(self):
        pass


class BusinessRegistrationTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson',
                     'email': 'test@test.app', 'password': '12345', 'password2': '12345',
                     'birth_date': '1991-04-20', "phone": '3458926930', 'city': 'Pavia', 'address': 'giovanni pellegrino',
                     'n_civ': '25', 'cap': '27100', 'cf': 'FRNGTN08R44L219V'}

    def test_can_create_business_user(self):
        response = self.client.post(reverse('account:register_business'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)       # TODO ADD check output and not only the status code !

    def test_can_update_fields(self):
        pass


