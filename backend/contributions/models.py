from django.db import models


class Contribution(models.Model):

    date = models.DateField(unique=True, blank=False, null=False)
    count = models.IntegerField()

    def __repr__(self):
        return 'Contribution(date={}, count={})'.format(self.date,
                                                        self.count)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_contribution_object(cls, value_object):
        return cls(date=value_object.date,
                   count=value_object.count)
