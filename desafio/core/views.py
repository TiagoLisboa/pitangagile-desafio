from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework_simplejwt.views import TokenObtainPairView

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

class SigninView(TokenObtainPairView):
    """
    API endpoint that allows users to signin.
    """
    serializer_class = SigninSerializer
