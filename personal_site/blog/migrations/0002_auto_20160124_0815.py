# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('text', tinymce.models.HTMLField()),
                ('tags', models.ManyToManyField(to='blog.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='percentage',
            field=models.IntegerField(default=0),
        ),
    ]
