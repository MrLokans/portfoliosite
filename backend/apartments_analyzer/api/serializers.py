from rest_framework import serializers

from apartments_analyzer.models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):

    price_USD = serializers.IntegerField(source='price')
    url = serializers.URLField(source='author_url')
    origin_url = serializers.URLField(source='bullettin_url')

    longitude = serializers.DecimalField(max_digits=None, decimal_places=None)
    latitude = serializers.DecimalField(max_digits=None, decimal_places=None)

    description = serializers.SerializerMethodField()

    def validate_description(self, value):
        return value

    class Meta:
        model = Apartment
        fields = ('price_USD', 'url', 'origin_url', 'address',
                  'longitude', 'latitude', 'description', )
