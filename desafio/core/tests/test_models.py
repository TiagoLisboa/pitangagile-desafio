from django.test import TestCase

from ..models import User

class UserTest(TestCase):
    """ Test module for User Model """

    def setUp(self):
        User.objects.create(firstName="John", lastName="Doe", email="johndoe@email.com", password="secret")
        User.objects.create(firstName="Jane", lastName="Doe", email="janedoe@email.com", password="secret")

    def test_user_full_name(self):
        john = User.objects.get(email="johndoe@email.com")
        jane = User.objects.get(email="janedoe@email.com")
        self.assertEqual(john.get_full_name(), "John Doe")
        self.assertEqual(jane.get_full_name(), "Jane Doe")

    def test_user_short_name(self):
        john = User.objects.get(email="johndoe@email.com")
        jane = User.objects.get(email="janedoe@email.com")
        self.assertEqual(john.get_short_name(), "John")
        self.assertEqual(jane.get_short_name(), "Jane")

