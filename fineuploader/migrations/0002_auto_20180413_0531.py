# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-13 05:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fineuploader', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temporary',
            name='file_obj',
        ),
        migrations.RemoveField(
            model_name='temporary',
            name='original_filename',
        ),
        migrations.RemoveField(
            model_name='temporary',
            name='uuid',
        ),
    ]
