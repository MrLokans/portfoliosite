from django.db import models


class PrecalculatedStatsQuerySet(models.QuerySet):
    def fetch_latest(self):
        return self.order_by('created_at').last()
