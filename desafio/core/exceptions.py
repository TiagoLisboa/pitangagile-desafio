from rest_framework.exceptions import PermissionDenied
from rest_framework import status

class CustomApiExceptions(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Exception'
    default_code = 'invalid'

    def __init__(self, message=None, status_code=None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.detail = {
            'message': self.message,
            'errorCode': self.status_code
        }


class InvalidFieldsException(CustomApiExceptions):
    message = 'Invalid Fields'


class MissingFieldsException(CustomApiExceptions):
    message = 'Missing Fields'


class EmailAlreadyExistsException(CustomApiExceptions):
    message = 'E-mail already exists'
