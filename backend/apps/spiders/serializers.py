from rest_framework import serializers

from apps.spiders import models


class SpiderEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpiderEvent
        fields = '__all__'
