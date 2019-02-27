from rest_framework import serializers

from ..models import Technology, Project, ProjectLink


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology

        fields = ["name", "general_description", "mastery_level"]


class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink

        fields = ["link", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)
    links = ProjectLinkSerializer(many=True)

    class Meta:
        model = Project
        fields = ["title", "description", "technologies", "links"]
