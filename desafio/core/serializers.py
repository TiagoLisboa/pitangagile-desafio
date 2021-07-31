from django.conf import settings

from .models import Phone
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['firstName', 'lastName', 'email', 'phones', 'created_at', 'last_login']


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['number', 'area_code', 'country_code']
