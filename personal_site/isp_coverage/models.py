from django.db import models


class ProviderCoords(models.Model):

    longitude = models.FloatField()
    latitude = models.FloatField()
