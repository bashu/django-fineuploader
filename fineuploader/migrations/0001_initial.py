# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-05 09:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import fineuploader.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temporary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formid', models.CharField(max_length=128)),
                ('field_name', models.CharField(blank=True, max_length=256, null=True)),
                ('file_obj', models.FileField(max_length=255, upload_to=fineuploader.models.upload_path, verbose_name='file')),
                ('original_filename', models.CharField(blank=True, max_length=255, null=True, verbose_name='original filename')),
                ('uuid', models.UUIDField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': 'temporary upload',
                'verbose_name_plural': 'temporary uploads',
            },
        ),
        migrations.AlterIndexTogether(
            name='temporary',
            index_together=set([('formid', 'field_name')]),
        ),
    ]
