# Generated by Django 2.0.8 on 2018-09-24 17:32

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('about_me', '0006_conferencetalkpage_intro'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceVideoLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('short_description', models.TextField()),
                ('video_url', models.URLField()),
                ('presentation_url', models.URLField()),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_links', to='about_me.ConferenceTalkPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
