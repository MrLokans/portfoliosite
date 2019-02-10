from typing import List

from rest_framework import serializers

from ..models import RentApartment, SoldApartments


class BaseApartmentSerializer(serializers.ModelSerializer):

    FIELD_NAME_MAP = (
        # Scrapy field, model field
        ('images', 'image_links'),
        ('origin_url', 'bullettin_url'),
        ('phones', 'user_phones'),
        ('user_url', 'author_url'),
    )

    class Meta:
        fields = ('price_USD', 'price_BYN', 'author_url', 'bullettin_url', 'address', 'apartment_type',
                  'longitude', 'latitude', 'description', 'image_links', 'user_phones', 'user_name',
                  'last_updated')

    longitude = serializers.DecimalField(max_digits=15, decimal_places=12)
    latitude = serializers.DecimalField(max_digits=15, decimal_places=12)

    @classmethod
    def validate_and_save(cls, input_data, **serializer_args):
        input_data = cls.perform_scrapy_data_transformation(input_data)
        item = cls(data=input_data, **serializer_args)
        item.is_valid(raise_exception=True)
        return item.save()

    @classmethod
    def perform_scrapy_data_transformation(cls, scrapy_data):
        scrapy_data = scrapy_data.copy()
        scrapy_data = cls._rename_scraped_fields(scrapy_data)
        scrapy_data['description'] = cls._clean_up_description(scrapy_data['description'])
        scrapy_data['image_links'] = cls._cleanup_image_links(scrapy_data['image_links'])
        return scrapy_data

    @classmethod
    def _clean_up_description(cls, text: List[str]) -> str:
        joined_text = " ".join(text).replace('\n', ' ')
        placed_pos = joined_text.find('Размещено')
        if placed_pos != -1:
            joined_text = joined_text[:placed_pos]
        return joined_text or ''

    @classmethod
    def _cleanup_image_links(cls, links: List[str]):
        return list(filter(bool, links))

    @classmethod
    def _rename_scraped_fields(cls, scrapped_data):
        for original_name, expected_model_name in cls.FIELD_NAME_MAP:
            scrapped_data[expected_model_name] = scrapped_data.pop(original_name)
        return scrapped_data

    def get_description(self, obj):
        return obj.description


class RentApartmentSerializer(BaseApartmentSerializer):
    """
    Defines a conversion layer between data generated
    by the scrapper and our internal database representation
    """

    class Meta:
        model = RentApartment
        fields = BaseApartmentSerializer.Meta.fields + \
                 ('has_balcony', 'has_conditioner', 'has_fridge', 'has_furniture', 'has_internet',
                  'has_kitchen_furniture', 'has_oven', 'has_tv', 'has_washing_machine',)


class SoldApartmentSerializer(BaseApartmentSerializer):
    class Meta:
        model = SoldApartments
        fields = BaseApartmentSerializer.Meta.fields + \
                 ('on_floor', 'total_floors', 'total_area', 'living_area', 'kitchen_area', 'house_type',
                  'balcony_details', 'parking_details', 'ceiling_details',)

    @classmethod
    def perform_scrapy_data_transformation(cls, scrapy_data):
        scrapy_data = super().perform_scrapy_data_transformation(scrapy_data)
        floors_data = scrapy_data.pop('floors')
        on_floor, total_floors = floors_data.split('/')
        scrapy_data['on_floor'] = int(on_floor)
        scrapy_data['total_floors'] = int(total_floors)
        scrapy_data['price_USD'] = int(scrapy_data['price_USD'].replace(' ', ''))
        scrapy_data['price_BYN'] = scrapy_data['price_BYN'].replace(' ', '')
        return scrapy_data

