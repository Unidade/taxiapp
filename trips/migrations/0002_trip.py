# Generated by Django 4.1.7 on 2023-04-03 20:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("trips", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Trip",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("pick_up_address", models.CharField(max_length=255)),
                ("drop_off_address", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("requested", "REQUESTED"),
                            ("started", "STARTED"),
                            ("IN_PROGRESS", "IN_PROGRESS"),
                            ("COMPLETED", "COMPLETED"),
                        ],
                        default="requested",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
