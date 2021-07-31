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
        user = User.objects.create(**validated_data)
        phones = [Phone(user=user, **phone) for phone in phones_data]
        phones = Phone.objects.bulk_create(phones)
        return user


class SigninSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)

        token['email'] = user.email
        return token

