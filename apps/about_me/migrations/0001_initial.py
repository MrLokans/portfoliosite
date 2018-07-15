# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('name', models.CharField(max_length=120)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='about_me.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('general_description', models.TextField()),
                ('mastery_level', models.IntegerField(choices=[(1, 'Novice'), (2, 'Intermediate'), (3, 'Advanced')], default=1)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(to='about_me.Technology'),
        ),
    ]