from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import permissions, generics, status, serializers
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


class SignupView(generics.CreateAPIView):
    """
    API endpoint that allows users to be created
    """
    queryset = User.objects.all()
    permission_class = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        email = request.data['email']
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise EmailAlreadyExistsException()

        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            raise InvalidFieldsException()
        except serializers.ValidationError as e:
            raise MissingFieldsException()
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
