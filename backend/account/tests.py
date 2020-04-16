import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .api.serializers import CustomerSerializer, BusinessSerializer
from .models import Customer, Business


class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin',
                                                       email='admin@gmail.com',
                                                       password='1234')

        self.data = {'username': 'mike', 'first_name': 'Mike', 'last_name': 'Tyson',
                     'email': 'test@test.app', 'password': '12345', 'password2': '12345',
                     "birth_date": "1994-04-20", "phone": "3458926930"}

    def test_can_create_user(self):
        response = self.client.post(reverse('account:register_customer'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_list_user(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('account:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_admin_list_user(self):
        self.client.force_login(User.objects.get_or_create(username='mike')[0])
        response = self.client.get(reverse('account:list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile(self):
        user = User.objects.get_or_create(username='mike')[0]
        self.client.force_login(user)
        response = self.client.get(reverse('account:list'), user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
