from rest_framework import serializers

from favorites.models import FavoriteLink


class FavoriteLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteLink
        fields = '__all__'
