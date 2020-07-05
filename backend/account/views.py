from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_email(user, order):
    subject, from_email, to, to_user = 'Nuovo Ordine Ricevuto', '"Marette" <marette.dev@gmail.com>', user.user.email, order.user.user.email

    html_content = render_to_string('order.html', {'username': user.user.username,
                                                    'order_date': order.date_created,
                                                    'order_products': order.items,
                                                    'order_menus': order.menus_items,
                                                    'order_total': order.get_total(),
                                                    'customer': order.user,
                                                    'restaurant': order.restaurant,
                                                   })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to, to_user])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=True)


def send_welcome_email(user, activation_token):

    subject, from_email, to = 'Benvenuto', '"Marette" <marette.dev@gmail.com>', user.email

    baseUrl = settings.EMAIL_ACTIVATE_ACCOUNT_BASE_URL

    html_content = render_to_string('welcome.html', {'username': user.username,
                                                     'baseUrl': baseUrl,
                                                     'id': user.id,
                                                     'activation_token': activation_token})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=True)


def send_reset_email(user, token):

    subject, from_email, to = 'Ripristino credenziali', '"Marette" <marette.dev@gmail.com>', user.email

    baseUrl = settings.EMAIL_RESET_PASSWORD_BASE_URL

    html_content = render_to_string('password-reset.html', {'username': user.username,
                                                            'baseUrl': baseUrl,
                                                            'id': user.id,
                                                            'token': token})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=True)
