from rest_framework.response import Response
from rest_framework import permissions, generics

from desafio.core.models import User
from desafio.core.serializers import UserSerializer

class UserView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(UserSerializer(user).data)



class SignupView(generics.CreateAPIView):
    """
    API endpoint that allows users to be created
    """
    queryset = User.objects.all()
    permission_class = (permissions.AllowAny,)
    serializer_class = UserSerializer
