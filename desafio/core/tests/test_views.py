from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework import status

from ..views import UserView
from ..exceptions import EmailAlreadyExistsException, InvalidFieldsException, MissingFieldsException

class UserViewTest(TestCase):
    """ Test module for UserView """

    def setUp(self):
        pass

    def test_get_object(self):
        user = AnonymousUser()
        req = RequestFactory().get('/me')

        req.user = user
        view = UserView(request=req)

        self.assertEquals(view.get_object(), user)

    def test_handle_exception_not_authenticated(self):
        view = UserView()
        response = view.handle_exception(NotAuthenticated())

        self.assertEquals(response.data, {
            'message': 'Unauthorized',
            'errorCode': status.HTTP_401_UNAUTHORIZED,
        })
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)



