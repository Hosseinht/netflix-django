# Generated by Django 3.2.12 on 2022-02-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="taggeditem",
            name="object_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
