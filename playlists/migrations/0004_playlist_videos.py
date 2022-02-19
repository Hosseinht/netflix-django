# Generated by Django 3.2.12 on 2022-02-19 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_alter_video_video_id'),
        ('playlists', '0003_playlist_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(blank=True, related_name='playlist_item', to='videos.Video'),
        ),
    ]
