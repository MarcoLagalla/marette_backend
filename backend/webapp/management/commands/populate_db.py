from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.crypto import get_random_string

from backend.account.models import Customer, Business
from backend.webapp.models.components import HomeComponent, VetrinaComponent, GalleriaComponent, EventiComponent, \
    MenuComponent, ContattaciComponent, RestaurantComponents
from backend.webapp.models.models import Restaurant, Product, Category, OrarioApertura, ProductTag


class Command(BaseCommand):
    help = 'populate DB with basic example data'

    def add_arguments(self, parser):
        parser.add_argument('-users', type=int, action='store', help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):

        # create ProductTag
        tags = ['Vegetariano', 'Vegano', 'GlutenFree', 'Piccante']
        for tag in tags:
            ProductTag.objects.create(name=tag)

        # create Customers
        customers_data = [
            {'user': {'username': 'prova', 'email': 'prova@tmp.it', 'first_name': 'Studente', 'last_name': 'Ripetente'},
             'password': '1234',
             'data': {'birth_date': '1995-08-29', 'phone': '+393456765999'}},

            {'user': {'username': 'marco', 'email': 'marcolagalla@yahoo.it', 'first_name': 'Marco', 'last_name': 'Lagalla'},
             'password': 'marco1234',
             'data': {'phone': '+393487665999'}, },

            {'user': {'username': 'clark95', 'email': 'clark@tmp.it', 'first_name': 'Clark', 'last_name': 'Kent'},
             'data': {'birth_date': '1995-08-29', 'phone': '+393490865999'}, },
        ]

        for customer in customers_data:

            with transaction.atomic():

                customer_user = User.objects.create(**customer['user'])
                try:
                    pwd = customer['password']
                except KeyError:
                    pwd = get_random_string()

                customer_user.set_password(pwd)
                customer_user.save()

                cus = Customer.objects.create(user=customer_user, **customer['data'],
                                              activation_token=get_random_string())
                cus.email_activated = True
                cus.save()

        # create categories

        categories = (  ('Pizzeria', 'Pizzeria'),
                        ('Ristorante', 'Ristorante'),
                        ('Fast food', 'Fast food'),
                        ('Gourmet', 'Gourmet'),
                        ('Birrificio', 'Birrificio'),
                        ('Mensa', 'Mensa'),
                        ('Paninoteca', 'Paninoteca'),
                        ('Bar', 'Bar'),
                        ('Piadineria', 'Piadineria'),
                        ('Osteria', 'Osteria'),
                        ('Trattoria', 'Trattoria'),
                        ('Tavola calda', 'Tavola calda'),
                        ('Pasticceria', 'Pasticceria'),
                        ('Etnico', 'Etnico'),   )

        for cat, cat1 in categories:
            Category.objects.create(category_name=cat)

        # CREATES Businesses and Restaurants

        business_data = [

            {'user': {'username': 'bulk', 'email': 'email1@tmp.it', 'first_name': 'Mario', 'last_name': 'Fabbrocini'},
             'data': {'cf': 'DLPNZE02T04A662J', 'birth_date': '1994-04-20', 'city': 'Torino',
                      'address': 'Via S Giovanni Bosco',
                      'n_civ': '9', 'cap': '15057', 'phone': '+393456765999'},
             'restaurant': [{'activity_name': 'Pizzeria l\'ancora', 'activity_description': 'Pizzeria storica napoletana',
                            'city': 'Napoli', 'address': 'Via o\'saraccino', 'n_civ': '98', 'cap': '15698',
                            'restaurant_number': '0131868956', 'p_iva': '11359591002'}]},

            {'user': {'username': 'pippo', 'email': 'email2@tmp.it', 'first_name': 'Pippo', 'last_name': 'Pluto'},
             'data': {'cf': 'LBRGRC05A14C351I', 'birth_date': '1994-05-05', 'city': 'Pavia',
                      'address': 'Pizza Duomo',
                      'n_civ': '21/A', 'cap': '15098', 'phone': '3288567993'}},

            {'user': {'username': 'luca', 'email': 'luca@tmp.it', 'first_name': 'Luca', 'last_name': 'Lagalla'},
             'data': {'cf': 'RLNRLF07D27F205S', 'birth_date': '2004-10-01', 'city': 'Tortona',
                      'address': 'Piazza Navona',
                      'n_civ': '278', 'cap': '14793', 'phone': '3288565678'}},

        ]

        for business in business_data:

            with transaction.atomic():

                business_user = User.objects.create(**business['user'])
                business_user.set_password(get_random_string())
                business_user.save()

                bus = Business.objects.create(user=business_user, **business['data'],
                                              activation_token=get_random_string())
                bus.email_activated = True
                bus.save()

                try:
                    for rest in business['restaurant']:

                        c = Category.objects.all().order_by('?').first()

                        restaurant = Restaurant.objects.create(owner=bus, **rest)
                        restaurant.restaurant_category.add(c)
                        restaurant.save()

                        home = HomeComponent.objects.create(restaurant=restaurant, name='HOME')
                        vetrina = VetrinaComponent.objects.create(restaurant=restaurant, name='VETRINA')
                        galleria = GalleriaComponent.objects.create(restaurant=restaurant, name='GALLERIA')
                        eventi = EventiComponent.objects.create(restaurant=restaurant, name='EVENTI')
                        menu = MenuComponent.objects.create(restaurant=restaurant, name='MENU')
                        contattaci = ContattaciComponent.objects.create(restaurant=restaurant, name='CONTATTI')

                        RestaurantComponents.objects.create(
                            restaurant=restaurant,
                            home=home,
                            vetrina=vetrina,
                            galleria=galleria,
                            eventi=eventi,
                            menu=menu,
                            contattaci=contattaci
                        )

                        # create TimeTable (empty)
                        OrarioApertura.objects.create(restaurant=restaurant)
                except KeyError:
                    pass

        print("DB Populated!")