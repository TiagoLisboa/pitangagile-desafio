from rest_framework.response import Response
from rest_framework import permissions, generics, status
from rest_framework.response import responses
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from desafio.core.models import User
from desafio.core.serializers import UserSerializer, SigninSerializer

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
        serializer.is_valid(raise_exception=True)
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

        token = serializer.validated_data
        return Response({
            'token': str(token['access']),
        }, status=status.HTTP_200_OK)
