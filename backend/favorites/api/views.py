from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from favorites.api.serializers import FavoriteLinkSerializer
from favorites.models import FavoriteLink


class FavoritesAPIView(ListCreateAPIView):
    serializer_class = FavoriteLinkSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_queryset(self):
        return FavoriteLink.objects.all()
