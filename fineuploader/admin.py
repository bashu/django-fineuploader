# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from attachments.admin import AttachmentInlines
from attachments.models import Attachment

from .models import Temporary


@admin.register(Temporary)
class TemporaryAdmin(admin.ModelAdmin):
    list_display = ['formid', 'count', 'timestamp']
    readonly_fields = ['formid', 'field_name', 'timestamp']
    date_hierarchy = 'timestamp'
    inlines = [AttachmentInlines]

    def count(self, obj):
        return Attachment.objects.attachments_for_object(obj).count()
    count.short_description = _("no. of attachments")
