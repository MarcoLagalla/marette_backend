from django.db import models
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class Message(models.Model):
    email = models.CharField(default='prova@email.com', max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField()


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url', 'subject', 'body', 'email', 'pk')
