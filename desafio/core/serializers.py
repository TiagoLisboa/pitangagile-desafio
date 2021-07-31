from django.conf import settings

from .models import Phone, User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'phones', 'created_at', 'last_login', 'password']
        read_only_fields = ['created_at', 'last_update']
        extra_kwargs = {'password': {'write_only': True}}


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['number', 'area_code', 'country_code']
