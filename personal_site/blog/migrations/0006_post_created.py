# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 2, 22, 17, 5, 50, 748892, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
