from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(user, activation_token):

    subject, from_email, to = 'Benvenuto', '"Marette" <staff@marette.ovh>', user.email

    baseUrl = settings.EMAIL_RESET_PASSWORD_BASE_URL

    html_content = render_to_string('welcome.html', {'username': user.username,
                                                     'baseUrl': baseUrl,
                                                     'id': user.id,
                                                     'activation_token': activation_token})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=True)


def send_reset_email(user, token):

    subject, from_email, to = 'Ripristino credenziali', '"Marette" <staff@marette.ovh>', user.email

    baseUrl = settings.EMAIL_RESET_PASSWORD_BASE_URL

    html_content = render_to_string('password-reset.html', {'username': user.username,
                                                            'baseUrl': baseUrl,
                                                            'id': user.id,
                                                            'token': token})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=True)