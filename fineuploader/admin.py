# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "content_object", "created")
    list_filter = ("content_type",)
    readonly_fields = ("uuid", "field_name", "created", "modified")
