import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .api.serializers import CustomerSerializer, BusinessSerializer, \
    CustomerRegistationSerializer, BusinessRegistationSerializer
from .models import Customer, Business


class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson',
                     'email': 'test@test.app', 'password': '12345', 'password2': '12345',
                     "birth_date": "1994-04-20", "cellphone_number": "3458926930"}

    def test_can_create_user(self):
        response = self.client.post(reverse('account:register_customer'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_list_user(self):
        self.superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('account:register_customer'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_admin_list_user(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        response = self.client.get(reverse('account:register_customer'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test(APITestCase):
    def test_customer_registration(self):
        data = {"username": "testcase", "email": "test@test.com", "password": "secret",
                "password2": "secret", "first_name": "foo", "last_name": "bar",
                "birth_date": "1994-04-20", "cellphone_number": "3458926930"}
        response = self.client.post("/api/v1/account/customer", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test for missing parameters
    def test_customer_wrong_registration(self):
        data = {"username": "testcase", "password": "secret",
                "password2": "secret_diff", "first_name": "foo",
                "birth_date": "1994-04-20", "cellphone_number": "3458926930"}
        response = self.client.post("/api/v1/account/customer", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_business_registration(self):
        data = {"username": "test_business", "email": "test_business@test.com", "password": "secret",
                "password2": "secret", "first_name": "foo", "last_name": "bar",
                "city": "London", "address": "Via S. Bosco", "cap": 15057,
                "activity_name": "ancora", "activity_description": "text",
                "url": "prova", "business_number": "3458926931"}
        response = self.client.post("/api/v1/account/business", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


