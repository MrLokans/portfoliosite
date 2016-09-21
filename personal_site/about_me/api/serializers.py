from rest_framework import serializers

from about_me.models import Technology


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology

        fields = [
            'name',
            'general_description',
            'mastery_level'
        ]
