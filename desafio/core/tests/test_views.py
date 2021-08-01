from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from ..views import UserView

class UserViewTest(TestCase):
    """ Test module for User Model """

    def setUp(self):
        pass

    def test_get_object(self):
        user = AnonymousUser()
        req = RequestFactory().get('/me')

        req.user = user
        view = UserView(request=req)

        self.assertEquals(view.get_object(), user)
