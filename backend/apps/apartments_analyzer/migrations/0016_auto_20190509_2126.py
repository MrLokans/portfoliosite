# Generated by Django 2.2.1 on 2019-05-09 18:26

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments_analyzer', '0015_usersearch_areas_of_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentapartment',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(0.0 0.0)', geography=True, srid=4326),
        ),
        migrations.AddField(
            model_name='soldapartments',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(0.0 0.0)', geography=True, srid=4326),
        ),
    ]