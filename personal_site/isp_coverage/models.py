from django.db import models


class Provider(models.Model):

    name = models.TextField(unique=True)
    url = models.CharField(max_length=120)


class ProviderCoordinate(models.Model):

    description = models.TextField(null=True, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    provider = models.ForeignKey(Provider)

    @classmethod
    def fromnamedtuple(cls, tpl, provider):
        return cls(longitude=tpl.longitude,
                   latitude=tpl.latitude,
                   description=tpl.latitude,
                   provider=provider)
