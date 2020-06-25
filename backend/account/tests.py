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

    # @classmethod
    # def setUpTestData(cls):
    def setUp(self):
        """ Static method for the access of a base customer user need to perform tests. """
        superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app', password=make_password('12345'))
        cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        base_customer = Customer.objects.create(user=base_user, **cust_user_data)

        self.datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789"}'

    def test_can_create_user(self):
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_user_with_notunique_username(self):
        datastr = self.datastr.replace('\n\t"username": "Lucci"', '\n\t"username": "mike"')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], "Esiste già un utente con questo username.")

    def test_cannot_create_user_with_wrong_email(self):
        datastr = self.datastr.replace('\n\t"email": "mail@email.it"','\n\t"email": "mail@"')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], "Inserisci un indirizzo email valido.")

    def test_cannot_create_user_with_notunique_email(self):
        datastr = self.datastr.replace('\n\t"email": "mail@email.it"','\n\t"email": "test@test.app"')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], "Esiste già un utente con questa email.")

    def test_cannot_create_user_with_wrong_confirm_psw(self):
        datastr = self.datastr.replace('\n\t"password2": "12345",', '\n\t"password2": "aaaaa",')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], "Le password devono combaciare.")

    def test_cannot_create_user_without_psw(self):
        datastr = self.datastr.replace('\n\t"password": "12345",', '\n\t"password": "",')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_user_with_invalid_phone(self):
        datastr = self.datastr.replace('\n\t"phone": "3456765789"', '\n\t"phone": "34567689"')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['phone'][0], "Il numero di telefono inserito non è valido.")

    def test_cannot_create_user_with_notunique_phone(self):
        datastr = self.datastr.replace('\n\t"phone": "3456765789"', '\n\t"phone": "3458926930"')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_customer'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['phone'][0], "Esiste già un utente con questo numero.")

    def test_can_logout_user(self):
        user = User.objects.get(username='mike')
        token, created = Token.objects.get_or_create(user=user)
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_no_admin_list_user(self):
        base_customer = User.objects.get(username='mike')  # or  id='2'
        self.client.force_login(base_customer)
        response = self.client.get(reverse('account:list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.content, b'{"detail":"Non hai l\'autorizzazione per eseguire questa azione."}')

    def test_user_profile(self):
        user = User.objects.get(username='mike')
        token, created = Token.objects.get_or_create(user=user)

        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(reverse('account:profile', kwargs={'id': user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['first_name'], "Mike")
        self.assertEqual(response.data['last_name'], "Tyson")
        self.assertEqual(response.data['phone'], "+393458926930")
        self.assertEqual(response.data['email'], "test@test.app")
        self.assertEqual(response.data['type'], "customer")

    def test_can_update_user(self):
        user = User.objects.get(username='mike')
        token, created = Token.objects.get_or_create(user=user)

        datastr = '{\n\t"first_name": "Mike1", \n\t"last_name": "Tyson1", \n\t"phone": "3456765700", ' \
                  '\n\t"birth_date": "1991-01-01"}'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(reverse('account:customer_update_profile', kwargs={'id': user.id}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "Mike1")
        self.assertEqual(response.data['last_name'], "Tyson1")
        self.assertEqual(response.data['phone'], "+393456765700")
        self.assertEqual(response.data['birth_date'], "1991-01-01")

    def test_can_update_user_password(self):
        pass
        # user = User.objects.get(username='mike')
        # token, created = Token.objects.get_or_create(user=user)
        #
        # datastr = '{\n\t"old_password": "12345", \n\t"new_password": "1234566", \n\t"new_password2": "1234566"}'
        # query_dict = QueryDict('', mutable=True)
        # query_dict.update({'data': datastr})
        #
        # self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        # response = self.client.put(reverse('account:change_password', kwargs={'id': user.id}), data=query_dict)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["password"], "password changed")
        # self._assert_contains(response.data["token"])
        #
        # # TODO VERIFY LOGIN WITH NEW CREDENTIALS


class BusinessRegistrationTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB', email='testB@test.app',
                                        password=make_password('12345'))
        buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
                            "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}
        base_business = Business.objects.create(user=base_user_b, **buss_user_data)

        self.datastr = '{\n\t"username": "Lucci", \n\t"email": "mail@email.it", \n\t"password": "12345", \n\t"password2": ' \
                  '"12345", \n\t"phone": "3456765789", \n\t"cf": "RNEMHL94P03F062G", \n\t"first_name": "michele22", ' \
                  '\n\t"last_name": "michele22", \n\t"birth_date": "1991-04-20", \n\t"city": "pavia", ' \
                  '\n\t"address": "marconi nuova", \n\t"n_civ": "25", \n\t"cap": "27100"}'

    def test_can_create_business_user(self):
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_business_user_with_invalid_cf(self):
        datastr = self.datastr.replace('\n\t"cf": "RNEMHL94P03F062G",', '\n\t"cf": "aaaaaaaaaaa",')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cf'][0], "Il codice fiscale non è valido.")

    def test_cannot_create_business_user_with_notunique_cf(self):
        datastr = self.datastr.replace('\n\t"cf": "RNEMHL94P03F062G",', '\n\t"cf": "FRNGTN08R44L219V",')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cf'][0], "Esiste già un utente con questo codice fiscale.")

    def test_cannot_create_business_user_without_city(self):
        datastr = self.datastr.replace("pavia", "")
    #    print(datastr)
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['city'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_business_user_without_address(self):
        datastr = self.datastr.replace('\n\t"address": "marconi nuova",', '\n\t"address": "",')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['address'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_business_user_without_n_civ(self):
        datastr = self.datastr.replace('\n\t"n_civ": "25",', '\n\t"n_civ": "",')
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': datastr})

        response = self.client.post(reverse('account:register_business'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['n_civ'][0], "Questo campo non può essere omesso.")

    def test_cannot_create_business_user_without_cap(self):
        datastr = self.datastr.replace('\n\t"cap": "27100"', '\n\t"cap": ""')
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


    def test_can_update_fields_business_user(self):
        pass

    def test_business_user_profile(self):
        pass