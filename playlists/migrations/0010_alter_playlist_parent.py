# Generated by Django 3.2.12 on 2022-03-06 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0009_alter_playlist_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gooz', to='playlists.playlist'),
        ),
    ]
