from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from personal_site.api.serializers import UserSerializer

User = get_user_model()


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer
