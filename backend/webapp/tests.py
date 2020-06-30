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
from .models.models import Restaurant, Category, Product
from django.test import Client
from ..account.tokens import account_activation_token


class RestaurantTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='1234')

        #base customer
        self.base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app',
                                        password=make_password('12345'))
        cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        self.base_customer = Customer.objects.create(user=self.base_user, **cust_user_data)
        self.base_customer_token = Token.objects.create(user=self.base_user)

        #base_business
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)

        buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)
       # print(self.base_business_token)

        # base_restaurant
        # rest_base_data = {"activity_name": "Pizzeria Ancora", "activity_description": "Tutto buonissimo",
        #                   "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100",
        #                   "p_iva": "IT01766920761", "restaurant_number": "3456765789"}

        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")
        # self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        # self.base_restaurant.restaurant_category.set([1, 2])
        # self.base_restaurant.set_url()

        self.datastr = '{\n\t"activity_name": "Bella napoli", \n\t"activity_description": "Tutta la pizza che vuoi", ' \
                       '\n\t"p_iva": "04113940409", \n\t"restaurant_number": "3456765689", ' \
                       '\n\t"city": "milano", \n\t"address": "marconi nuova", \n\t"n_civ": "2", \n\t"cap": "27100", ' \
                       '\n\t"restaurant_category": '

    def test_business_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                             'token': str(
                                                                                 self.base_business.activation_token)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')


    def test_business_can_create_restaurant(self):
        # Need to activate the email first
        self.test_business_can_activate_email()

        # Register the restaurants
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr + str([1,2]) + '}'})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_business_can_create_another_restaurant(self):
        self.test_business_can_activate_email()      # Need to activate the email first
        self.test_business_can_create_restaurant()   # Need to create a first restaurant

        # change a bit the restaurant data to respect unique constraints
        self.datastr = self.datastr.replace('\n\t"activity_name": "Bella napoli",', '\n\t"activity_name": "Pizza Pazza",')
        self.datastr = self.datastr.replace('\n\t"n_civ": "2",', '\n\t"n_civ": "26",')

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr + str([1,2]) + '}'})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_no_email_activated_business_can_create_restaurant(self):
        # NOT activate the email !!!
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr})
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_business_can_create_restaurant(self):
        user = User.objects.get(username='mike')
        token, created = Token.objects.get_or_create(user=user)

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_customer_token))
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_list_restaurant(self):
        self.test_business_can_create_restaurant()
        response = self.client.get(reverse('webapp:list_restaurants'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_show_restaurant(self):
        self.test_business_can_create_restaurant()
        restaurant = Restaurant.objects.get(activity_name="Bella napoli")
        response = self.client.get(reverse('webapp:show_restaurant', kwargs={'id': restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_name'], "Bella napoli")
        self.assertEqual(response.data['p_iva'], "04113940409")

    def test_can_owner_update_restaurant_fields(self):
        self.test_business_can_create_restaurant()

        # change a bit the restaurant fields to update
        self.datastr = self.datastr.replace('\n\t"activity_name": "Bella napoli",',
                                            '\n\t"activity_name": "Pizza Pazza",')
        self.datastr = self.datastr.replace('\n\t"n_civ": "2",', '\n\t"n_civ": "26",')
        self.datastr = self.datastr.replace('\n\t"restaurant_number": "3456765689",',
                                            '\n\t"restaurant_number": "3444765689",')

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr + str([1, 2]) + '}'})

        restaurant = Restaurant.objects.get(activity_name="Bella napoli")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:update_restaurant', kwargs={'id': restaurant.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activity_name'], "Pizza Pazza")
        self.assertEqual(response.data['n_civ'], "26")
        self.assertEqual(response.data['restaurant_number'], "+393444765689")

    def test_can_anyone_show_category_list(self):
        response = self.client.get(reverse('webapp:category_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['category_name'], "bar")
        self.assertEqual(response.data[1]['category_name'], "pizzeria")


    def test_can_owner_delete_restaurants(self):
        self.test_business_can_create_restaurant()

        restaurant = Restaurant.objects.get(activity_name="Bella napoli")
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'confirm': str(restaurant.url)})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:delete_restaurant', kwargs={'id': restaurant.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Ristorante cancellato.")

    def test_can_no_customer_delete_others_restaurants(self):
        self.test_business_can_create_restaurant()

        restaurant = Restaurant.objects.get(activity_name="Bella napoli")
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'confirm': str(restaurant.url)})

        self.client.force_login(self.base_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_customer_token))
        response = self.client.post(reverse('webapp:delete_restaurant', kwargs={'id': restaurant.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Non hai l'autorizzazione per eseguire questa azione.")

    def test_can_customer_vote_restaurant(self):
        self.test_business_can_create_restaurant()
        self.base_customer.email_activated = True

        restaurant = Restaurant.objects.get(activity_name="Bella napoli")
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'vote': str(5)})

        self.client.force_login(self.base_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_customer_token))
        response = self.client.post(reverse('webapp:vote_restaurant', kwargs={'id': restaurant.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], "Grazie per aver votato questo ristorante.")





class RestaurantProductsTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='1234')

        #base customer
        self.base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app',
                                        password=make_password('12345'))
        cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        self.base_customer = Customer.objects.create(user=self.base_user, **cust_user_data)
        self.base_customer_token = Token.objects.create(user=self.base_user)

        #base_business
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)

        buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)
       # print(self.base_business_token)

        # base_restaurant
        rest_base_data = {"activity_name": "Pizzeria Ancora", "activity_description": "Tutto buonissimo",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100",
                          "p_iva": "IT01766920761", "restaurant_number": "3456765789"}

        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")

        # ProductTag.objects.create(name="Vegano", description="Cibo vegano, no carne")
        # ProductTag.objects.create(name="Gluten Free", description="Senza glutine")

        self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        self.base_restaurant.restaurant_category.set([1, 2])
        self.base_restaurant.set_url()

        self.datastr = '{\n\t"activity_name": "Bella napoli", \n\t"activity_description": "Tutta la pizza che vuoi", ' \
                       '\n\t"p_iva": "04113940409", \n\t"restaurant_number": "3456765689", ' \
                       '\n\t"city": "milano", \n\t"address": "marconi nuova", \n\t"n_civ": "2", \n\t"cap": "27100", ' \
                       '\n\t"restaurant_category": '

    def test_business_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                             'token': str(
                                                                                 self.base_business.activation_token)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

    def test_business_can_add_product(self):
        self.test_business_can_activate_email()

        data = '{\n\t"name": "Pizza diavola", \n\t"description": "Diavola più diavola non si può", ' \
               '\n\t"price": "6.50", \n\t"iva": "22", \n\t"category": "Pizza"}'

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': data})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:add_product', kwargs={'id': self.base_restaurant.pk}),
                                    data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Pizza diavola")
        self.assertEqual(response.data['final_price'], "6.50")

    def test_business_can_remove_product(self):
        self.test_business_can_activate_email()
        self.test_business_can_add_product()

        data = '{\n\t"name": "Pizza diavola", \n\t"description": "Diavola più diavola non si può", ' \
               '\n\t"price": "6.50", \n\t"iva": "22", \n\t"category": "Pizza"}'

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': data})

        product = Product.objects.get(name="Pizza diavola")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:delete_product', kwargs={'id': self.base_restaurant.pk,
                                                                             'p_id': product.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Prodotto eliminato correttamente")

    def test_business_can_update_product(self):
        self.test_business_can_activate_email()
        self.test_business_can_add_product()

        data = '{\n\t"name": "Pizza margherita", \n\t"description": "Una margherita cosi non l avete mai vista", ' \
               '\n\t"price": "4.50", \n\t"iva": "22", \n\t"category": "Pizza"}'

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': data})

        product = Product.objects.get(name="Pizza diavola")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:update_product', kwargs={'id': self.base_restaurant.pk,
                                                                             'p_id': product.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Pizza margherita")
        self.assertEqual(response.data['description'], "Una margherita cosi non l avete mai vista")
        self.assertEqual(response.data['final_price'], "4.50")

    def test_anyone_can_list_product(self):
        self.test_business_can_add_product()
        response = self.client.get(reverse('webapp:list_products', kwargs={'id': self.base_restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Pizza'][0]['name'], "Pizza diavola")
        self.assertEqual(response.data['Pizza'][0]['price'], "6.50")

    def test_anyone_can_show_product(self):
        self.test_business_can_add_product()
        product = Product.objects.get(name="Pizza diavola")
        response = self.client.get(reverse('webapp:details_product', kwargs={'id': self.base_restaurant.pk,
                                                                             'p_id': product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Pizza diavola")
        self.assertEqual(response.data['price'], "6.50")


class RestaurantSearchTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='1234')

        #base customer
        self.base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app',
                                        password=make_password('12345'))
        cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        self.base_customer = Customer.objects.create(user=self.base_user, **cust_user_data)
        self.base_customer_token = Token.objects.create(user=self.base_user)

        #base_business
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)

        buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)
       # print(self.base_business_token)

        # base_restaurant
        # rest_base_data = {"activity_name": "Pizzeria Ancora", "activity_description": "Tutto buonissimo",
        #                   "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100",
        #                   "p_iva": "IT01766920761", "restaurant_number": "3456765789"}

        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")
        # self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        # self.base_restaurant.restaurant_category.set([1, 2])
        # self.base_restaurant.set_url()

        self.datastr = '{\n\t"activity_name": "Bella napoli", \n\t"activity_description": "Tutta la pizza che vuoi", ' \
                       '\n\t"p_iva": "04113940409", \n\t"restaurant_number": "3456765689", ' \
                       '\n\t"city": "milano", \n\t"address": "marconi nuova", \n\t"n_civ": "2", \n\t"cap": "27100", ' \
                       '\n\t"restaurant_category": '

    def test_business_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                             'token': str(
                                                                                 self.base_business.activation_token)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')


    def test_business_can_create_restaurant(self):
        # Need to activate the email first
        self.test_business_can_activate_email()

        # Register the restaurants
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr + str([1,2]) + '}'})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



#
#
# class RestaurantTimeTableTestCase(APITestCase):
#
#     def setUp(self):
#       #  self.superuser = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='1234')
#
#         # #base customer
#         # self.base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app',
#         #                                 password=make_password('12345'))
#         # cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
#         # self.base_customer = Customer.objects.create(user=self.base_user, **cust_user_data)
#         # self.base_customer_token = Token.objects.create(user=self.base_user)
#
#         #base_business
#         self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
#                                           email='testB@test.app', password=make_password('12345'))
#         base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)
#
#         buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
#                           "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}
#         self.base_business = Business.objects.create(user=self.base_user_b,
#                                                      activation_token=base_user_b_activation_token,**buss_user_data)
#         self.base_business_token = Token.objects.create(user=self.base_user_b)
#         self.base_business.email_activated = True
#        # print(self.base_business_token)
#
#         #base_restaurant
#         rest_base_data = {"activity_name": "Pizzeria Ancora", "activity_description": "Tutto buonissimo",
#                           "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100",
#                           "p_iva": "IT01766920761", "restaurant_number": "3456765789"}
#
#         c1 = Category.objects.create(category_name="bar")
#         c2 = Category.objects.create(category_name="pizzeria")
#         self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
#         self.base_restaurant.restaurant_category.set([1, 2])
#         self.base_restaurant.set_url()
#
#         self.datastr = '{\n\t"activity_name": "Bella napoli", \n\t"activity_description": "Tutta la pizza che vuoi", ' \
#                        '\n\t"p_iva": "04113940409", \n\t"restaurant_number": "3456765689", ' \
#                        '\n\t"city": "milano", \n\t"address": "marconi nuova", \n\t"n_civ": "2", \n\t"cap": "27100", ' \
#                        '\n\t"restaurant_category": '
#
#     # def test_business_can_activate_email(self):
#     #     response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
#     #                                                                          'token': str(
#     #                                                                              self.base_business.activation_token)}))
#     #
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')
#
#     def test_business_can_activate_email(self):
#         response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
#                                                                              'token': str(
#                                                                                  self.base_business.activation_token)}))
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')
#
#     def test_owner_can_add_day_to_TimeTable(self):
#         self.test_business_can_activate_email()
#
#         data = '{\n\t"Lunedi": 1}'
#         query_dict = QueryDict('', mutable=True)
#         query_dict.update({'day': "('Lunedi', 'Lunedi')"})
#
#         self.client.force_login(self.base_user_b)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
#         response = self.client.post(reverse('webapp:create_opening_day', kwargs={'id': self.base_restaurant.pk}), data=query_dict)
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

