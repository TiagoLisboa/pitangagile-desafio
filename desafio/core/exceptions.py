from rest_framework.exceptions import PermissionDenied
from rest_framework import status

class InvalidFieldsException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'message': 'Invalid Fields',
        'errorCode': 400,
    }
    default_code = 'invalid'

    def __init__(self, message=None, status_code=None):
        if message is not None:
            self.default_detail['message'] = message
        if status_code is not None:
            self.status_code = status_code
            self.default_detail['errorCode'] = status_code
        self.detail = self.default_detail


class MissingFieldsException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'message': 'Missing Fields',
        'errorCode': 400,
    }
    default_code = 'invalid'

    def __init__(self, message=None, status_code=None):
        if message is not None:
            self.default_detail['message'] = message
        if status_code is not None:
            self.status_code = status_code
            self.default_detail['errorCode'] = status_code
        self.detail = self.default_detail


class EmailAlreadyExistsException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        'message': 'E-mail already exists',
        'errorCode': 400,
    }
    default_code = 'invalid'

    def __init__(self, message=None, status_code=None):
        if message is not None:
            self.default_detail['message'] = message
        if status_code is not None:
            self.status_code = status_code
            self.default_detail['errorCode'] = status_code
        self.detail = self.default_detail
