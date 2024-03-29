# Generated by Django 3.2.12 on 2022-02-20 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("videos", "0002_auto_20220220_0822"),
        ("playlists", "0003_auto_20220220_1420"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="playlists.playlist",
            ),
        ),
        migrations.AlterField(
            model_name="playlist",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="playlist_featured",
                to="videos.video",
            ),
        ),
    ]
