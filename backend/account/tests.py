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
    user = None

    @classmethod
    def setUpTestData(cls):
        superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app', password=make_password('12345'))

        base_customer = Customer.objects.create(user=base_user, **data)


    def setUp(self):
        pass


    def test_can_create_user(self):                                                  # TODO NON SALVA EFFETTIVAMENTE GLI UTENTI NEL DB
        response = self.client.post(reverse('account:register_customer'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)            # TODO ADD check output and not only the status code !
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data['username'], self.data['username'])
        self.assertTrue(response.data['token'], response.data['id'])

        self.user = User.objects.get_or_create(username='mike')[0]


    def test_can_logout_user(self):
        user = User.objects.get_or_create(username='mike')[0]        # cosi crea un utente alla cazzum
        #self.client.force_login(user)

        token, created = Token.objects.get_or_create(user=user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_login_user(self):

        #print(self.user)
        #self.test_can_create_user()

        json_data = json.dumps({"email": 'test@test.app', "password": "12345"})
        response2 = self.client.post(reverse('account:login'), json_data, content_type="application/json")

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        print(response2.data['token'])
        self.assertTrue(response2.data['token'])

    def test_admin_list_user(self):
        response = self.client.post(reverse('account:register_customer'), self.data)
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # TODO ADD check output and not only the status code !
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data['username'], self.data['username'])
        self.assertTrue(response.data['token'], response.data['id'])



        self.client.force_login(self.superuser)
        response = self.client.get(reverse('account:list'))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    # TODO NON VA BENE RIPORTA UNA SCRITTA VUOTA
        self.assertGreater(len(response.data), 0)

    def test_no_admin_list_user(self):
        user = User.objects.get_or_create(username='mike')[0]
        self.client.force_login(user)
        #self.client.force_login(User.objects.get_or_create(username='mike')[0])
        response = self.client.get(reverse('account:list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)   # TODO ADD check error msg output and not only the status code !

    def test_user_profile(self):
        pass
        # user = User.objects.get_or_create(username='mike')[0]
        # print(user, user.id, user.phone)
        # token, created = Token.objects.get_or_create(user=user)
        # self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        # response = self.client.get('api/v1/account/profile/' + str(user.id))
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




#self.assertEqual(response.content, '{"username": "lauren", "id": 4}')
