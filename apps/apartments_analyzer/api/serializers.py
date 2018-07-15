from rest_framework import serializers

from ..models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    """
    Defines a conversion layer between data generated
    by the scrapper and our internal database representation
    """
    class Meta:
        model = Apartment
        fields = ('price_USD', 'price_BYN', 'author_url', 'bullettin_url', 'address', 'apartment_type',
                  'longitude', 'latitude', 'description', 'image_links', 'user_phones', 'user_name',
                  'last_updated',
                  'has_balcony', 'has_conditioner', 'has_fridge', 'has_furniture', 'has_internet',
                  'has_kitchen_furniture', 'has_oven', 'has_tv', 'has_washing_machine', )

    longitude = serializers.DecimalField(max_digits=15, decimal_places=12)
    latitude = serializers.DecimalField(max_digits=15, decimal_places=12)

    def get_description(self, obj):
        return obj.description

    def create(self, validated_data):
        apartment = Apartment.objects.create(**validated_data)
        return apartment

    def update(self, instance, validated_data):
        return instance
