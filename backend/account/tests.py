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

    def test_customer_registration(self):
        data = {"username": "testcase", "email": "test@test.com", "password": "secret",
                "password2": "secret", "first_name": "foo", "last_name": "bar",
                "birth_date": "1994-04-20", "cellphone_number": "3458926930"}
        response = self.client.post("/api/v1/account/customer", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_business_registration(self):
        data = {"username": "test_business", "email": "test_business@test.com", "password": "secret",
                "password2": "secret", "first_name": "foo", "last_name": "bar",
                "city": "London", "address": "Via S. Bosco", "cap": 15057,
                "activity_name": "ancora", "activity_description": "text",
                "url": "prova", "business_number": "3458926931"}
        response = self.client.post("/api/v1/account/business", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


