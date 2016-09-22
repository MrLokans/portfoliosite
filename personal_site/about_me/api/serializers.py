from rest_framework import serializers

from about_me.models import Technology, Project


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology

        fields = [
            'name',
            'general_description',
            'mastery_level'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'technologies'
        ]
