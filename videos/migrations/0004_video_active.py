# Generated by Django 3.2.12 on 2022-02-18 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_videoproxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]