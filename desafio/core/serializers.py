from .models import Phone, User
from rest_framework import serializers


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ['number', 'area_code', 'country_code']


class UserSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True)
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'phones', 'created_at', 'last_login', 'password']
        read_only_fields = ['created_at', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

