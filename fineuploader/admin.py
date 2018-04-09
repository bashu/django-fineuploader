# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Temporary


@admin.register(Temporary)
class TemporaryAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'timestamp']
    readonly_fields = ['formid', 'field_name', 'timestamp']
    date_hierarchy = 'timestamp'
