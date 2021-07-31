from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from desafio.core.serializers import UserSerializer, PhoneSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PhoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows phones to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [permissions.IsAuthenticated]
