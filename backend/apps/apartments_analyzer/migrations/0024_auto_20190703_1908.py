# Generated by Django 2.2.1 on 2019-07-03 16:08

import operator
from functools import reduce

from django.db import migrations
from django.db.models import Q

AGENT_NAME_SIGNS = ['По факту', 'агент', 'агентство', 'OOO', 'ООО']
NON_AGENT_SIGNS = ['не агент', ]


def detect_possible_agents(apps, schema_editor):
    # May run for quite a long time
    RentApartment = apps.get_model('apartments_analyzer', 'RentApartment')
    SoldApartments = apps.get_model('apartments_analyzer', 'SoldApartments')
    agent_filter = reduce(operator.or_, [Q(user_name__icontains=v)
                                           for v in AGENT_NAME_SIGNS])
    non_agent_filter = reduce(operator.or_, [Q(user_name__icontains=v)
                                             for v in NON_AGENT_SIGNS])
    agents_query = agent_filter & ~non_agent_filter
    for model in [RentApartment, SoldApartments]:
        model.objects.filter(agents_query).update(likely_agent=True)
        model.objects.filter(~agents_query).update(likely_agent=False)


class Migration(migrations.Migration):

    dependencies = [
        ('apartments_analyzer', '0023_auto_20190703_1907'),
    ]

    operations = [
        migrations.RunPython(detect_possible_agents),
    ]