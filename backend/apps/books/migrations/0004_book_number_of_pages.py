# Generated by Django 2.0.4 on 2018-06-02 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20180521_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='number_of_pages',
            field=models.IntegerField(default=0),
        ),
    ]
