from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

User = get_user_model()


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
