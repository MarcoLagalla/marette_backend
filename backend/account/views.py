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

def send_welcome_email(user):

    msg = MIMEMultipart('alternative')
    password = settings.EMAIL_HOST_PASSWORD
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email
    msg['Subject'] = "Welcome to Marette"

    html_content = render_to_string('welcome.html', {'username': user.username})  # render with dynamic value
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

# def send_welcome_email(user):
#
#     gmail_user = settings.EMAIL_HOST_USER
#     gmail_password = settings.EMAIL_HOST_PASSWORD
#     gmail_server = settings.EMAIL_HOST
#     gmail_port = settings.EMAIL_PORT
#
#     try:
#
#         # # Create message container - the correct MIME type is multipart/alternative.
#         # msg = MIMEMultipart('alternative')
#         # msg['Subject'] = "Welcome on Marette"
#         # msg['From'] = settings.DEFAULT_FROM_EMAIL
#         # msg['To'] = user.email
#         #
#         html_content = render_to_string('welcome.html', {'username': user.username})  # render with dynamic value
#         text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
#         # part1 = MIMEText(text_content, 'html')
#         # msg.attach(part1)
#
#         server = smtplib.SMTP(gmail_server, gmail_port)
#         server.ehlo()
#         server.starttls()
#         server.ehlo()
#         server.login(gmail_user, gmail_password)
#         server.sendmail(settings.EMAIL_HOST_USER, user.email, "ciaooo")
#         server.quit()
#
#     except Exception as err:
#         print(err)