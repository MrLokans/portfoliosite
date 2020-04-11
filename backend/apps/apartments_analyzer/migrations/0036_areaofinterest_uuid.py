# Generated by Django 3.0.4 on 2020-04-11 07:24

from django.db import migrations, models
import uuid


def create_uuids(apps, schema_editor):
    Area = apps.get_model('apartments_analyzer', 'AreaOfInterest')
    for area in Area.objects.all():
        area.uuid = uuid.uuid4()
        area.save()


class Migration(migrations.Migration):

    dependencies = [
        ('apartments_analyzer', '0035_cityregion_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaofinterest',
            name='uuid',
            field=models.UUIDField(blank=True, null=True, default=uuid.uuid4),
        ),
        migrations.RunPython(create_uuids),
        migrations.AlterField(
            model_name='areaofinterest',
            name='uuid',
            field=models.UUIDField(unique=True, default=uuid.uuid4),
        )
    ]