# Generated by Django 2.2.1 on 2019-05-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments_analyzer', '0014_auto_20190509_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersearch',
            name='areas_of_interest',
            field=models.ManyToManyField(to='apartments_analyzer.AreaOfInterest'),
        ),
    ]