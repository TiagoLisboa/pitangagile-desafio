from django.test import TestCase

from ..serializers import UserSerializer
from ..models import Phone, User


class UserSerializerTest(TestCase):
    """ Test Module for User serializer """

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
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password('secret'))
        self.assertEquals(user.phones.count(), 1)
        for phone in user.phones.all():
            self.assertIsInstance(phone, Phone)
            self.assertDictContainsSubset(
                {'number': 123456789, 'area_code': 13, 'country_code': '+55'},
                phone.__dict__
            )


