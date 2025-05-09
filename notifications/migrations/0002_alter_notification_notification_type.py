# Generated by Django 5.1.4 on 2024-12-27 22:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("message", "New Message"),
                    ("property", "Property Update"),
                    ("follow", "New Follower"),
                    ("like", "New Like"),
                    ("comment", "New Comment"),
                    ("comment_like", "Comment Like"),
                    ("comment_reply", "Comment Reply"),
                ],
                max_length=20,
            ),
        ),
    ]
