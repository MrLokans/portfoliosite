from rest_framework import serializers

from apartments_analyzer.models import Apartment, ApartmentImage


class ApartmentImageSerializer(serializers.RelatedField):

    def to_representation(self, obj):
        return obj.image_url

    def to_internal_value(self, value):
        return value


class ApartmentSerializer(serializers.ModelSerializer):

    price_USD = serializers.IntegerField(source='price')
    url = serializers.URLField(source='author_url')
    origin_url = serializers.URLField(source='bullettin_url')

    longitude = serializers.DecimalField(max_digits=None, decimal_places=None)
    latitude = serializers.DecimalField(max_digits=None, decimal_places=None)

    description = serializers.CharField()
    images = ApartmentImageSerializer(many=True,
                                      queryset=Apartment.objects.all())

    def get_description(self, obj):
        # TODO: Add actual description transformation
        return obj.description

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        apartment = Apartment.objects.create(**validated_data)
        for image_url in images_data:
            ApartmentImage.objects.create(apartment=apartment,
                                          image_url=image_url)
        return apartment

    class Meta:
        model = Apartment
        fields = ('price_USD', 'url', 'origin_url', 'address',
                  'longitude', 'latitude', 'description', 'images')
