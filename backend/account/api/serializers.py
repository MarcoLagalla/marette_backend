from rest_framework import serializers
from backend.account.models import CustomerUser
from django.contrib.auth import get_user_model

User = get_user_model()