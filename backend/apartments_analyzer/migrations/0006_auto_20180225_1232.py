# Generated by Django 2.0.2 on 2018-02-25 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments_analyzer', '0005_historicalapartment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalapartment',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalApartment',
        ),
    ]