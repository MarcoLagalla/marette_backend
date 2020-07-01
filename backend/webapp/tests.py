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
from .models.models import Restaurant, Category, Product, ProductDiscount
from .models.menu import Menu, MenuEntry
from django.test import Client
from ..account.tokens import account_activation_token


rest_base_data = {"activity_name": "Pizzeria Ancora", "activity_description": "Tutto buonissimo",
                  "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100",
                  "p_iva": "IT01766920761", "restaurant_number": "3456765789"}

buss_user_data = {"birth_date": "1994-04-20", "phone": "3458926930", "cf": "FRNGTN08R44L219V",
                          "city": "Pavia", "address": "marconi nuova", "n_civ": "25", "cap": "27100"}

datastr = '{\n\t"activity_name": "Bella napoli", \n\t"activity_description": "Tutta la pizza che vuoi", ' \
                       '\n\t"p_iva": "04113940409", \n\t"restaurant_number": "3456765689", ' \
                       '\n\t"city": "milano", \n\t"address": "marconi nuova", \n\t"n_civ": "2", \n\t"cap": "27100", ' \
                       '\n\t"restaurant_category": '


class RestaurantTestCase(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@gmail.com', password='1234')

        #base customer
        self.base_user = User.objects.create(username='mike', first_name='Mike', last_name='Tyson', email='test@test.app',
                                        password=make_password('12345'))
        self.base_user_activation_token = account_activation_token.make_token(user=self.base_user)
        cust_user_data = {"birth_date": "1994-04-20", "phone": "3458926930"}
        self.base_customer = Customer.objects.create(user=self.base_user, **cust_user_data)
        self.base_customer_token = Token.objects.create(user=self.base_user)

        #base_business
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)

        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")

        self.datastr = datastr

    def test_business_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                    'token': str(self.base_business.activation_token)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

    def test_customer_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user.id,
                                                                'token': str(self.base_user_activation_token)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

    def test_business_can_create_restaurant(self):
        self.test_business_can_activate_email()

        # Register the restaurants
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr + str([1, 2]) + '}'})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_business_can_create_another_restaurant(self):
        self.test_business_can_create_restaurant()   # Need to create a first restaurant

        # change a bit the restaurant data to respect unique constraints
        self.datastr = self.datastr.replace('\n\t"activity_name": "Bella napoli",', '\n\t"activity_name": "Pizza Pazza",')
        self.datastr = self.datastr.replace('\n\t"n_civ": "2",', '\n\t"n_civ": "26",')

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr + str([1, 2]) + '}'})

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
        self.test_customer_can_activate_email()        #needed if not activated he can't vote

        restaurant = Restaurant.objects.get(activity_name="Bella napoli")
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'vote': str(5)})

        self.client.force_login(self.base_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_customer_token))
        response = self.client.post(reverse('webapp:vote_restaurant', kwargs={'id': restaurant.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'][0], "Grazie per aver votato questo ristorante.")

    def test_cannot_customer_vote_restaurant_without_activated_mail(self):
        self.test_business_can_create_restaurant()

        restaurant = Restaurant.objects.get(activity_name="Bella napoli")
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'vote': str(5)})

        self.client.force_login(self.base_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_customer_token))
        response = self.client.post(reverse('webapp:vote_restaurant', kwargs={'id': restaurant.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RestaurantProductsTestCase(APITestCase):

    def setUp(self):
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)

        # base_restaurant
        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")

        # ProductTag.objects.create(name="Vegano", description="Cibo vegano, no carne")
        # ProductTag.objects.create(name="Gluten Free", description="Senza glutine")

        self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        self.base_restaurant.restaurant_category.set([1, 2])
        self.base_restaurant.set_url()

        self.datastr = datastr

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
        self.test_business_can_add_product()

        product = Product.objects.get(name="Pizza diavola")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:delete_product', kwargs={'id': self.base_restaurant.pk,
                                                                             'p_id': product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Prodotto eliminato correttamente")

    def test_can_business_update_product(self):
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

    def test_can_anyone_list_product(self):
        self.test_business_can_add_product()
        response = self.client.get(reverse('webapp:list_products', kwargs={'id': self.base_restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Pizza'][0]['name'], "Pizza diavola")
        self.assertEqual(response.data['Pizza'][0]['price'], "6.50")

    def test_can_anyone_show_product(self):
        self.test_business_can_add_product()
        product = Product.objects.get(name="Pizza diavola")
        response = self.client.get(reverse('webapp:details_product', kwargs={'id': self.base_restaurant.pk,
                                                                             'p_id': product.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Pizza diavola")
        self.assertEqual(response.data['price'], "6.50")


class RestaurantProductDiscountsTestCase(APITestCase):

    def setUp(self):
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)

        # base_restaurant
        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")

        self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        self.base_restaurant.restaurant_category.set([1, 2])
        self.base_restaurant.set_url()

        self.datastr = datastr

    def test_business_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                             'token': str(
                                                                                 self.base_business.activation_token)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

    def test_business_can_add_product_discount_percentuale(self):
        self.test_business_can_activate_email()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({"title": "Sconti Pazzi", "type": "Percentuale", "value": "60"})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:add_discounts', kwargs={'id': self.base_restaurant.pk}),
                                    data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Sconti Pazzi")
        self.assertEqual(response.data['type'], "Percentuale")
        self.assertEqual(response.data['value'], "60.00")

    def test_business_can_add_product_discount_fisso(self):
        self.test_business_can_activate_email()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({"title": "Sconto studenti 5eu", "type": "Fisso", "value": "5"})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:add_discounts', kwargs={'id': self.base_restaurant.pk}),
                                    data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Sconto studenti 5eu")
        self.assertEqual(response.data['type'], "Fisso")
        self.assertEqual(response.data['value'], "5.00")

    def test_business_can_remove_product_discount_percentuale(self):
        self.test_business_can_add_product_discount_percentuale()

        productDiscount = ProductDiscount.objects.get(title="Sconti Pazzi")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:delete_discounts', kwargs={'id': self.base_restaurant.pk,
                                                                             'd_id': productDiscount.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_business_can_remove_product_discount_fisso(self):
        self.test_business_can_add_product_discount_fisso()

        productDiscount = ProductDiscount.objects.get(title="Sconto studenti 5eu")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:delete_discounts', kwargs={'id': self.base_restaurant.pk,
                                                                             'd_id': productDiscount.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_business_update_product_discount(self):
        self.test_business_can_add_product_discount_fisso()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({"title": "Sconto lavoratori 10eu", "type": "Fisso", "value": "10"})

        productDiscount = ProductDiscount.objects.get(title="Sconto studenti 5eu")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:edit_discounts', kwargs={'id': self.base_restaurant.pk,
                                                                        'd_id': productDiscount.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        productDiscount = ProductDiscount.objects.get(title="Sconto lavoratori 10eu")
        self.assertEqual(productDiscount.title, "Sconto lavoratori 10eu")
        self.assertEqual(productDiscount.type, "Fisso")
        self.assertEqual(str(productDiscount.value), "10.00")

    def test_can_anyone_list_product_discount(self):
        self.test_business_can_add_product_discount_fisso()
        self.test_business_can_add_product_discount_percentuale()

        response = self.client.get(reverse('webapp:list_discounts', kwargs={'id': self.base_restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Sconti Pazzi")
        self.assertEqual(response.data[0]['type'], "Percentuale")
        self.assertEqual(response.data[0]['value'], "60.00")

        self.assertEqual(response.data[1]['title'], "Sconto studenti 5eu")
        self.assertEqual(response.data[1]['type'], "Fisso")
        self.assertEqual(response.data[1]['value'], "5.00")

    def test_can_anyone_show_product_discount(self):
        self.test_business_can_add_product_discount_fisso()
        productDiscount = ProductDiscount.objects.get(title="Sconto studenti 5eu")
        response = self.client.get(reverse('webapp:details_discounts', kwargs={'id': self.base_restaurant.pk,
                                                                             'd_id': productDiscount.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Sconto studenti 5eu")
        self.assertEqual(response.data['type'], "Fisso")
        self.assertEqual(response.data['value'], "5.00")


class RestaurantMenuTestCase(APITestCase):

    def setUp(self):
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)

        # base_restaurant
        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")

        self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        self.base_restaurant.restaurant_category.set([1, 2])
        self.base_restaurant.set_url()

        self.datastr = datastr

    def test_business_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                             'token': str(
                                                                                 self.base_business.activation_token)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

    def test_business_can_add_menu(self):
        self.test_business_can_activate_email()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({"name": "Menu del giorno", "price": "12.0", "iva": "22", "description": "Daily menu"})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:add_menu', kwargs={'id': self.base_restaurant.pk}),
                                    data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Menu del giorno")
        self.assertEqual(response.data['iva'], 22)

    def test_business_can_remove_menu(self):
        self.test_business_can_add_menu()

        menu = Menu.objects.get(name="Menu del giorno")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:delete_menu', kwargs={'id': self.base_restaurant.pk,
                                                                             'm_id': menu.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_business_update_menu(self):
        self.test_business_can_add_menu()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({"name": "Menu della domenica", "price": "15.0", "iva": "22", "description": "Daily menu"})

        menu = Menu.objects.get(name="Menu del giorno")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:edit_menu', kwargs={'id': self.base_restaurant.pk,
                                                                             'm_id': menu.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        menu = Menu.objects.get(name="Menu della domenica")
        self.assertEqual(menu.name, "Menu della domenica")
        self.assertEqual(str(menu.price), "15.00")

    def test_can_anyone_list_restaurant_menu(self):
        self.test_business_can_add_menu()
        response = self.client.get(reverse('webapp:list_menus', kwargs={'id': self.base_restaurant.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "Menu del giorno")
        self.assertEqual(str(response.data[0]['price']), "12.00")

    def test_can_anyone_show_restaurant_menu(self):
        self.test_business_can_add_menu()
        menu = Menu.objects.get(name="Menu del giorno")
        response = self.client.get(reverse('webapp:details_menu', kwargs={'id': self.base_restaurant.pk,
                                                                             'm_id': menu.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Menu del giorno")
        self.assertEqual(str(response.data['price']), "12.00")


class RestaurantMenuEntryTestCase(APITestCase):

    def setUp(self):
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)

        # base_restaurant
        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")

        self.base_restaurant = Restaurant.objects.create(owner_id=self.base_business.pk, **rest_base_data)
        self.base_restaurant.restaurant_category.set([1, 2])
        self.base_restaurant.set_url()

        self.datastr = datastr

    def test_business_can_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                             'token': str(
                                                                                 self.base_business.activation_token)}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

    def test_business_can_add_menu(self):
        self.test_business_can_activate_email()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({"name": "Menu del giorno", "price": "12.0", "iva": "22", "description": "Daily menu"})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:add_menu', kwargs={'id': self.base_restaurant.pk}),
                                    data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Menu del giorno")
        self.assertEqual(response.data['iva'], 22)

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

    def test_business_can_add_menu_entry(self):
        self.test_business_can_add_menu()
        self.test_business_can_add_product()

        menu = Menu.objects.get(name="Menu del giorno")
        product = Product.objects.get(name="Pizza diavola")

        query_dict = QueryDict('', mutable=True)
        query_dict.update({"name": "Menu del giorno", "num_products": 5, "products": str(product.pk)})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:add_menuentry', kwargs={'id': self.base_restaurant.pk,
                                                                    'm_id': menu.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Menu del giorno")
        self.assertEqual(response.data['num_products'], 5)
        self.assertEqual(response.data['id'], product.pk)

    def test_business_can_remove_menu_entry(self):
        self.test_business_can_add_menu_entry()

        menu = Menu.objects.get(name="Menu del giorno")
        menuentry = MenuEntry.objects.get(name="Menu del giorno")

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:delete_menuentry', kwargs={'id': self.base_restaurant.pk,
                                                                             'm_id': menu.pk,
                                                                             'me_id': menuentry.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_business_update_menu_entry(self):
        self.test_business_can_add_menu_entry()

        menu = Menu.objects.get(name="Menu del giorno")
        product = Product.objects.get(name="Pizza diavola")
        menuentry = MenuEntry.objects.get(name="Menu del giorno")

        data = '{\n\t"name": "Menu del weekend", \n\t"num_products": "2"'
        query_dict = QueryDict('', mutable=True)
        query_dict.update({"name": "Menu del weekend", "num_products": "2"})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:edit_menuentry', kwargs={'id': self.base_restaurant.pk,
                                                             'm_id': menu.pk, 'me_id': menuentry.pk}), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        menuentry = MenuEntry.objects.get(name="Menu del weekend")
        self.assertEqual(menuentry.name, "Menu del weekend")
        self.assertEqual(str(menuentry.num_products), "2")

    def test_can_anyone_show_restaurant_menu_entry(self):
        self.test_business_can_add_menu_entry()
        menu = Menu.objects.get(name="Menu del giorno")
        menuentry = MenuEntry.objects.get(name="Menu del giorno")

        response = self.client.get(reverse('webapp:details_menuentry', kwargs={'id': self.base_restaurant.pk,
                                                                             'm_id': menu.pk, 'me_id': menuentry.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Menu del giorno")
        self.assertEqual(str(response.data['num_products']), "5")


class RestaurantSearchTestCase(APITestCase):

    def setUp(self):
        self.base_user_b = User.objects.create(username='mikeB', first_name='MikeB', last_name='TysonB',
                                          email='testB@test.app', password=make_password('12345'))
        base_user_b_activation_token = account_activation_token.make_token(user=self.base_user_b)
        self.base_business = Business.objects.create(user=self.base_user_b,
                                                     activation_token=base_user_b_activation_token,**buss_user_data)
        self.base_business_token = Token.objects.create(user=self.base_user_b)

        c1 = Category.objects.create(category_name="bar")
        c2 = Category.objects.create(category_name="pizzeria")

        self.datastr = datastr

    def test_can_business_activate_email(self):
        response = self.client.get(reverse('account:activate_email', kwargs={'id': self.base_user_b.id,
                                                                'token': str(self.base_business.activation_token)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['activation'], 'Indirizzo email confermato, account attivo.')

    def test_business_can_create_restaurant(self):
        # Need to activate the email first
        self.test_can_business_activate_email()

        # Register the restaurants
        query_dict = QueryDict('', mutable=True)
        query_dict.update({'data': self.datastr + str([1,2]) + '}'})

        self.client.force_login(self.base_user_b)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.base_business_token))
        response = self.client.post(reverse('webapp:register_restaurant'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_anyone_search_restaurant_by_name(self):
        self.test_business_can_create_restaurant()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'query': 'Bella napoli'})

        response = self.client.get(reverse('webapp:search_restaurant_query'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['activity_name'], "Bella napoli")
        self.assertEqual(response.data['results'][0]['city'], "milano")

    def test_can_anyone_search_restaurant_by_wrong_name(self):
        self.test_business_can_create_restaurant()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'query': 'Pizzeria da gigi'})

        response = self.client.get(reverse('webapp:search_restaurant_query'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'][0], "Nessun Ristorante trovato.")

    def test_can_anyone_search_restaurant_by_city(self):
        self.test_business_can_create_restaurant()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'city': 'milano'})

        response = self.client.get(reverse('webapp:search_restaurant_query'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['activity_name'], "Bella napoli")
        self.assertEqual(response.data['results'][0]['city'], "milano")

    def test_can_anyone_search_restaurant_by_name_and_city(self):
        self.test_business_can_create_restaurant()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'query': 'Bella napoli', 'city': 'milano'})

        response = self.client.get(reverse('webapp:search_restaurant_query'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['activity_name'], "Bella napoli")
        self.assertEqual(response.data['results'][0]['city'], "milano")

    def test_can_anyone_search_restaurant_by_category(self):
        self.test_business_can_create_restaurant()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'restaurant_category': 'pizzeria'})

        response = self.client.get(reverse('webapp:search_restaurant_query'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['activity_name'], "Bella napoli")
        self.assertEqual(response.data['results'][0]['city'], "milano")

    def test_can_anyone_search_restaurant_by_name_and_city_and_category(self):
        self.test_business_can_create_restaurant()

        query_dict = QueryDict('', mutable=True)
        query_dict.update({'query': 'Bella napoli', 'city': 'milano', 'restaurant_category': 'pizzeria'})

        response = self.client.get(reverse('webapp:search_restaurant_query'), data=query_dict)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['activity_name'], "Bella napoli")
        self.assertEqual(response.data['results'][0]['city'], "milano")







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

