# Generated by Django 3.2.16 on 2022-12-19 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_rename_name_user_display_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="enabled",
            field=models.BooleanField(default=True),
        ),
    ]
