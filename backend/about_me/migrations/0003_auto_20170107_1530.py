# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-07 15:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about_me', '0002_auto_20161015_1738'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='technology',
            options={'verbose_name_plural': 'technologies'},
        ),
    ]