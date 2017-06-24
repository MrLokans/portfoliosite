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

    description = serializers.CharField(allow_blank=True)
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

    def update(self, instance, validated_data):
        images_data = set(validated_data.pop('images'))
        existing_images = set(ApartmentImage.objects\
            .filter(apartment=instance)\
            .values_list('image_url', flat=True))
        new_images = images_data - existing_images
        removed_images = existing_images - images_data

        # If photos added to the apartment page
        # we create it in the database
        ApartmentImage.objects.bulk_create([
            ApartmentImage(**{'image_url': image_url,
                              'apartment': instance})
            for image_url in new_images
        ])
        # If removed - delete it accordingly
        ApartmentImage.objects\
            .filter(apartment=instance,
                    image_url__in=removed_images)\
            .delete()
        return instance

    class Meta:
        model = Apartment
        fields = ('price_USD', 'url', 'origin_url', 'address',
                  'longitude', 'latitude', 'description', 'images')
