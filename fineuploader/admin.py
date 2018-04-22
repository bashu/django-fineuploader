# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Attachment


class AttachmentInlines(GenericStackedInline):
    model = Attachment
    exclude = ()
    extra = 1


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content_object', 'timestamp')
    list_filter = ('content_type',)
    readonly_fields = ('uuid', 'field_name', 'timestamp')
