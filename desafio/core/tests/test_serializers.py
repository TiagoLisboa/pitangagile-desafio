from django.test import TestCase
from unittest import mock

from ..serializers import UserSerializer, SigninSerializer
from ..models import Phone, User


class UserSerializerTest(TestCase):
    """ Test Module for UserSerializer """

    def setUp(self) -> None:
        return super().setUp()

    def test_create_user_serializer(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'secret',
            'phones': [
                {'number': 123456789, 'area_code': 13, 'country_code': '+55'}
            ]
        }
        serializer = UserSerializer(data=data)

        is_valid = serializer.is_valid(raise_exception=True)
        self.assertTrue(is_valid)

        with mock.patch('desafio.core.serializers.update_last_login') as mock_update_last_login:
            user = serializer.save()
        mock_update_last_login.assert_called()

        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password('secret'))
        self.assertEquals(user.phones.count(), 1)

        for phone in user.phones.all():
            self.assertIsInstance(phone, Phone)
            self.assertDictContainsSubset(
                {'number': 123456789, 'area_code': 13, 'country_code': '+55'},
                phone.__dict__
            )


class SigninSerializerTest(TestCase):
    """ Test Module for SigninSerializer """

    def setUp(self) -> None:
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'secret',
            'phones': []
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        self.user = serializer.instance
        return super().setUp()

    def test_signin_serializer_get_token(self):
        serializer = SigninSerializer(self.user)
        token = serializer.get_token(self.user)
        self.assertEquals(token['email'], self.user.email)

    def test_signin_serializer_validate(self):
        serializer = SigninSerializer(data={
            'email': 'johndoe@email.com',
            'password': 'secret'
        })
        with mock.patch('desafio.core.serializers.update_last_login') as mock_update_last_login:
            serializer.is_valid()

        mock_update_last_login.assert_called()

