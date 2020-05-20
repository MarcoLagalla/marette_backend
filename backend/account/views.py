from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(user, activation_token):

    subject, from_email, to = 'Benvenuto', '"Marette" <staff@marette.ovh>', user.email

    html_content = render_to_string('welcome.html', {'username': user.username,
                                                     'id': user.id,
                                                     'token': activation_token})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def send_reset_email(user, token):

    subject, from_email, to = 'Ripristino credenziali', '"Marette" <staff@marette.ovh>', user.email

    html_content = render_to_string('password-reset.html', {'username': user.username,
                                                            'id': user.id,
                                                            'token': token})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()