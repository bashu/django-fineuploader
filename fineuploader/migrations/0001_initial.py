# Generated by Django 2.1.10 on 2019-07-03 10:53

import django.db.models.deletion
import django.utils.timezone
import positions.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("attachments", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "attachment_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="attachments.Attachment",
                    ),
                ),
                ("field_name", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "original_filename",
                    models.CharField(blank=True, max_length=255, null=True, verbose_name="original filename"),
                ),
                ("uuid", models.UUIDField()),
                ("position", positions.fields.PositionField(default=-1, verbose_name="order")),
            ],
            options={
                "verbose_name": "attachment",
                "verbose_name_plural": "attachments",
                "ordering": ["-created", "position"],
            },
            bases=("attachments.attachment",),
        ),
        migrations.CreateModel(
            name="Temporary",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("formid", models.CharField(max_length=128)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={"verbose_name": "temporary", "verbose_name_plural": "temporary", "ordering": ["-timestamp"]},
        ),
    ]
