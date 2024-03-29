# Generated by Django 3.2.12 on 2022-02-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("playlists", "0005_tvshowproxy_tvshowseasonproxy"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlist",
            name="type",
            field=models.CharField(
                choices=[
                    ("MOV", "Movie"),
                    ("TVS", "TV Show"),
                    ("SEA", "Season"),
                    ("PLA", "Playlist"),
                ],
                default="PLA",
                max_length=3,
            ),
        ),
    ]
