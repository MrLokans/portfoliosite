# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-15 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('about_me', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlink',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='about_me.Project'),
        ),
    ]