# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Upload


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'timestamp']
    readonly_fields = ['formid', 'field_name', 'timestamp']
    date_hierarchy = 'timestamp'
