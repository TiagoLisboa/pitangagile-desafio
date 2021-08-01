from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Phone, User


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

    def create(self, validated_data):
        phones_data = validated_data.pop('phones')
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        phones = [Phone(user=user, **phone) for phone in phones_data]
        phones = Phone.objects.bulk_create(phones)
        return user


class SigninSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)

        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        update_last_login(None, self.user)

        return data

