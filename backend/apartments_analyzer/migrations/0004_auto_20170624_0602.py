# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-24 06:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments_analyzer', '0003_auto_20170623_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='id',
        ),
        migrations.AlterField(
            model_name='apartment',
            name='bullettin_url',
            field=models.URLField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='description',
            field=models.TextField(),
        ),
    ]
