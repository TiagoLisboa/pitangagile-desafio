from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, ErrorDetail
from rest_framework import status, serializers
from unittest import mock

from rest_framework_simplejwt.tokens import RefreshToken

from ..views import SigninView, UserView, SignupView
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

    def test_handle_exception_authentication_failed(self):
        view = UserView()
        response = view.handle_exception(AuthenticationFailed())

        self.assertEquals(response.data, {
            'message': 'Unauthorized - invalid session',
            'errorCode': status.HTTP_401_UNAUTHORIZED,
        })
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SignupViewTest(TestCase):
    """ Test module for SignupView """

    def setUp(self):
        pass

    def test_unpack_validation_errors_email_unique(self):
        view = SignupView()
        validation_error_detail = {
            'email': [ErrorDetail('test', 'unique')]
        }
        with self.assertRaises(EmailAlreadyExistsException):
            view.unpack_validation_errors(validation_error_detail)

    def test_unpack_validation_errors_required(self):
        view = SignupView()
        validation_error_detail = {
            'email': [ErrorDetail('test', 'required')]
        }
        with self.assertRaises(MissingFieldsException):
            view.unpack_validation_errors(validation_error_detail)

    def test_unpack_validation_errors_invalid(self):
        view = SignupView()
        validation_error_detail = {
            'email': [ErrorDetail('test', 'invalid')]
        }
        with self.assertRaises(InvalidFieldsException):
            view.unpack_validation_errors(validation_error_detail)

    def test_create(self):
        view = SignupView()
        request = RequestFactory().get('/signup')
        request.data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'secret',
            'phones': []
        }
        with mock.patch('desafio.core.views.SignupView.get_serializer') as get_serializer:
            with mock.patch('desafio.core.views.SignupView.perform_create') as perform_create:
                with mock.patch('desafio.core.views.RefreshToken') as refresh_token:
                    serializer = mock.Mock()
                    serializer.is_valid = mock.Mock(return_value=True)
                    get_serializer.return_value = serializer

                    token = mock.MagicMock()
                    token.access_token = 'token_string'
                    refresh_token.for_user = mock.Mock(return_value=token)

                    resp = view.create(request)

                    self.assertEquals(resp.data, { 'token': 'token_string'})
                    serializer.is_valid.assert_called()
                    perform_create.assert_called()

    def test_create_validation_error(self):
        view = SignupView()
        request = RequestFactory().get('/signup')
        request.data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'secret',
            'phones': []
        }
        with mock.patch('desafio.core.views.SignupView.get_serializer') as get_serializer:
            with mock.patch('desafio.core.views.SignupView.unpack_validation_errors') as unpack_validation_errors:
                serializer = mock.Mock()
                serializer.is_valid = mock.Mock(side_effect=serializers.ValidationError)
                get_serializer.return_value = serializer

                resp = view.create(request)

                serializer.is_valid.assert_called()
                unpack_validation_errors.assert_called()


class SigninViewTest(TestCase):
    """ Test module for SigninView """

    def setUp(self):
        pass

    def test_post_validation_error(self):
        view = SigninView()
        request = RequestFactory().get('/signin')
        request.data = {
            'email': 'johndoe@email.com',
            'password': 'secret',
        }
        with mock.patch('desafio.core.views.SigninView.get_serializer') as get_serializer:
            serializer = mock.Mock()
            serializer.is_valid = mock.Mock(side_effect=serializers.ValidationError)
            get_serializer.return_value = serializer

            with self.assertRaises(MissingFieldsException):
                view.post(request=request)

            serializer.is_valid.assert_called()

    def test_post_authentication_failed_error(self):
        view = SigninView()
        request = RequestFactory().get('/signin')
        request.data = {
            'email': 'johndoe@email.com',
            'password': 'secret',
        }
        with mock.patch('desafio.core.views.SigninView.get_serializer') as get_serializer:
            serializer = mock.Mock()
            serializer.is_valid = mock.Mock(side_effect=AuthenticationFailed)
            get_serializer.return_value = serializer

            with self.assertRaises(InvalidFieldsException):
                view.post(request=request)

            serializer.is_valid.assert_called()
