import json

from django.http import QueryDict
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

    def test_can_create_user(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_user_with_wrong_email(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], "Inserisci un indirizzo email valido.")

    def test_cannot_create_user_with_notunique_email(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "test@test.app", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], "Esiste già un utente con questa email.")

    def test_cannot_create_user_with_wrong_confirm_psw(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@alt2.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"aaaaaa", \n\t"phone": "3456765789"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], "Le password devono combaciare.")

    def test_cannot_create_user_without_psw(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@alt2.it", \n\t"password": "", \n\t"password2": ' \
                  '"", \n\t"phone": "3456765789"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_user_with_invalid_phone(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@alt2.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "34567689"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['phone'][0], "Il numero di telefono inserito non è valido.")

    def test_can_logout_user(self):
        user = User.objects.get(username='mike')
        token, created = Token.objects.get_or_create(user=user)
       # print("LOGOUT TOKEN = ", token.key)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_login_user(self):
        json_data = json.dumps({"email": 'test@test.app', "password": "12345"})
        response = self.client.post(reverse('account:login'), json_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(username='mike')
        token, created = Token.objects.get_or_create(user=user)
        self.assertEqual(response.data['token'], str(token))

    def test_cannot_login_user_with_wrong_credentials(self):
        json_data = json.dumps({"email": 'test@test.app', "password": "aaaaaa"})
        response = self.client.post(reverse('account:login'), json_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], ["Credenziali sbagliate."])

    def test_admin_list_user(self):
        superuser = User.objects.get_or_create(username='admin')[0]
        self.client.force_login(superuser)
        response = self.client.get(reverse('account:list'))
    #    print(response.data)
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

    def test_can_update_user_password(self):
        pass


class BusinessRegistrationTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        base_user = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB', email='testB@test.app',
                                        password=make_password('12345'))

        # self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson',
        #              'email': 'test@test.app', 'password': '12345', 'password2': '12345',
        #              'birth_date': '1991-04-20', "phone": '3458926930', 'city': 'Pavia', 'address': 'giovanni pellegrino',
        #              'n_civ': '25', 'cap': '27100', 'cf': 'FRNGTN08R44L219V'}

    def test_can_create_business_user(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789", \n\t"cf": "RNEMHL94P03F062G", \n\t"first_name": "michele22", ' \
                  '\n\t"last_name": "michele22", \n\t"birth_date": "1991-04-20", \n\t"city": "Pavia", ' \
                  '\n\t"address": "marconi nuova", \n\t"n_civ": "25", \n\t"cap": "27100"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_business_user_with_invalid_cf(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789", \n\t"cf": "aaaaaaaaaaa", \n\t"first_name": "michele22", ' \
                  '\n\t"last_name": "michele22", \n\t"birth_date": "1991-04-20", \n\t"city": "Pavia", ' \
                  '\n\t"address": "marconi nuova", \n\t"n_civ": "25", \n\t"cap": "27100"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cf'][0], "Il codice fiscale non è valido.")

    def test_cannot_create_business_user_without_city(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789", \n\t"cf": "RNEMHL94P03F062G", \n\t"first_name": "michele22", ' \
                  '\n\t"last_name": "michele22", \n\t"birth_date": "1991-04-20", \n\t"city": "", ' \
                  '\n\t"address": "marconi nuova", \n\t"n_civ": "25", \n\t"cap": "27100"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['city'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_business_user_without_address(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789", \n\t"cf": "RNEMHL94P03F062G", \n\t"first_name": "michele22", ' \
                  '\n\t"last_name": "michele22", \n\t"birth_date": "1991-04-20", \n\t"city": "pavia", ' \
                  '\n\t"address": "", \n\t"n_civ": "25", \n\t"cap": "27100"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['address'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_business_user_without_n_civ(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789", \n\t"cf": "RNEMHL94P03F062G", \n\t"first_name": "michele22", ' \
                  '\n\t"last_name": "michele22", \n\t"birth_date": "1991-04-20", \n\t"city": "pavia", ' \
                  '\n\t"address": "ponte impero", \n\t"n_civ": "", \n\t"cap": "27100"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['n_civ'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_business_user_without_cap(self):
        datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789", \n\t"cf": "RNEMHL94P03F062G", \n\t"first_name": "michele22", ' \
                  '\n\t"last_name": "michele22", \n\t"birth_date": "1991-04-20", \n\t"city": "pavia", ' \
                  '\n\t"address": "ponte impero", \n\t"n_civ": "2", \n\t"cap": ""}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cap'][0], "È richiesto un numero intero valido.")

    def test_can_login_business_user(self):
        json_data = json.dumps({"email": 'testB@test.app', "password": "12345"})
        response = self.client.post(reverse('account:login'), json_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(username='mikeB')
        token, created = Token.objects.get_or_create(user=user)
        self.assertEqual(response.data['token'], str(token))


    def test_can_update_fields(self):
        pass
