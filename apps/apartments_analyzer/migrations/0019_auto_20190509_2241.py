# Generated by Django 2.2.1 on 2019-05-09 19:41

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments_analyzer', '0018_auto_20190509_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaofinterest',
            name='poly',
            field=django.contrib.gis.db.models.fields.PolygonField(geography=True, srid=4326),
        ),
        migrations.CreateModel(
            name='SearchResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reported_urls', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None)),
                ('search_filter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='apartments_analyzer.UserSearch')),
            ],
            options={
                'verbose_name_plural': 'Reported search results',
            },
        ),
    ]
