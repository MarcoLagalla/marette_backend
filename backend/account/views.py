from rest_framework import viewsets
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMessage, get_connection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_welcome_email(user, activation_token):

    msg = MIMEMultipart('alternative')
    password = settings.EMAIL_HOST_PASSWORD
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email
    msg['Subject'] = "Welcome to Marette"

    html_content = render_to_string('welcome.html', {'username': user.username,
                                                     'id': user.id,
                                                     'activation_token': activation_token})
    # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
    part1 = MIMEText(text_content, 'plain')
    msg.attach(part1)
    part2 = MIMEText(html_content, 'html')
    msg.attach(part2)

    server = smtplib.SMTP('{0}: {1}'.format(settings.EMAIL_HOST, settings.EMAIL_PORT))
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def send_reset_email(user,token):
    msg = MIMEMultipart('alternative')
    password = settings.EMAIL_HOST_PASSWORD
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email
    msg['Subject'] = "Marette Password Reset"

    html_content = render_to_string('password-reset.html', {'username': user.username,
                                                     'id': user.id,
                                                     'token': token})
    # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
    part1 = MIMEText(text_content, 'plain')
    msg.attach(part1)
    part2 = MIMEText(html_content, 'html')
    msg.attach(part2)

    server = smtplib.SMTP('{0}: {1}'.format(settings.EMAIL_HOST, settings.EMAIL_PORT))
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()