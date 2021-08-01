from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import permissions, generics, status, serializers
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from desafio.core.models import User
from desafio.core.serializers import UserSerializer, SigninSerializer
from desafio.core.exceptions import EmailAlreadyExistsException, InvalidFieldsException, MissingFieldsException

class UserView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def handle_exception(self, exc):
        if isinstance(exc, NotAuthenticated):
            return Response({
                'message': 'Unauthorized',
                'errorCode': exc.status_code,
            }, exc.status_code)

        if isinstance(exc, AuthenticationFailed):
            return Response({
                'message': 'Unauthorized - invalid session',
                'errorCode': exc.status_code,
            }, exc.status_code)


        return super().handle_exception(exc)


class SignupView(generics.CreateAPIView):
    """
    API endpoint that allows users to be created
    """
    queryset = User.objects.all()
    permission_class = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def unpack_validation_errors(self, validation_error_detail):
        for error in validation_error_detail:
            for errorDetail in validation_error_detail[error]:
                if isinstance(errorDetail, dict):
                    self.unpack_validation_errors(errorDetail)
                else:
                    if error == 'email' and errorDetail.code == 'unique':
                        raise EmailAlreadyExistsException()
                    if errorDetail.code == 'required':
                        raise MissingFieldsException()
        raise InvalidFieldsException()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            self.unpack_validation_errors(e.detail)

        self.perform_create(serializer)
        token = RefreshToken.for_user(serializer.instance)

        return Response({
            'token': str(token.access_token),
        }, status.HTTP_201_CREATED)


class SigninView(TokenObtainPairView):
    """
    API endpoint that allows users to signin.
    """
    serializer_class = SigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except AuthenticationFailed as e:
            raise InvalidFieldsException('Invalid e-mail or password')
        except serializers.ValidationError as e:
            raise MissingFieldsException()

        token = serializer.validated_data
        return Response({
            'token': str(token['access']),
        }, status=status.HTTP_200_OK)
