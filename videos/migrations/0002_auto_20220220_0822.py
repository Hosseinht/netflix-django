# Generated by Django 3.2.12 on 2022-02-20 04:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("videos", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoAllProxy",
            fields=[],
            options={
                "verbose_name": "All Video",
                "verbose_name_plural": "All Videos",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("videos.video",),
        ),
        migrations.CreateModel(
            name="VideoPublishedProxy",
            fields=[],
            options={
                "verbose_name": "Published Video",
                "verbose_name_plural": "Published Videos",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("videos.video",),
        ),
        migrations.AddField(
            model_name="video",
            name="active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="video",
            name="publish_timestamp",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="video",
            name="state",
            field=models.CharField(
                choices=[("PU", "Publish"), ("DR", "Draft")], default="DR", max_length=2
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(2022, 2, 20, 4, 52, 48, 10994, tzinfo=utc),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="video",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="video",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="video",
            name="video_id",
            field=models.CharField(max_length=220, unique=True),
        ),
    ]
