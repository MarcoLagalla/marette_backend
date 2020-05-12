from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework import serializers

from django.contrib.auth.models import User
from backend.webapp.models.orders import Order


READ_CHOICES = (
        ('U', 'Unread'),
        ('R', 'Read'),
    )


class OrderNotification(models.Model):
    issued = models.DateTimeField(auto_created=True, auto_now_add=True)
    recipient = models.ForeignKey(User, related_name='restaurant_owner', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=READ_CHOICES)
    message = models.CharField(max_length=300)

    def __str__(self):
        return "[{0}] - {1}".format(self.recipient, self.message)