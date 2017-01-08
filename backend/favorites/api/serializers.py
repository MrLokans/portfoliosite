from rest_framework import serializers

from favorites.models import FavoriteLink


class FavoriteLinkSerializer(serializers.ModelSerializer):

    url = serializers.URLField(max_length=320)

    class Meta:
        model = FavoriteLink
        fields = '__all__'
