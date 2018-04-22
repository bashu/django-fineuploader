# -*- coding: utf-8 -*-

import os
import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.files import File
from django.core.urlresolvers import get_callable
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import ugettext_lazy as _

from positions.fields import PositionField

from .conf import settings
from .managers import AttachmentManager


def upload_path(instance, filename):
    FILENAME_FUNCTION = getattr(
        settings, 'FINEUPLOADER_FILENAME_FUNCTION', None)

    func = FILENAME_FUNCTION
    if func is None:
        func = lambda x: x

    if isinstance(func, str):
        func = get_callable(func)

    return os.path.join(
        'attachments',
        instance.content_object._meta.app_label,
        instance.content_object._meta.object_name.lower(),
        str(instance.content_object.pk),
        func(filename),
    )


@python_2_unicode_compatible
class Attachment(models.Model):

    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=128)
    content_object = GenericForeignKey('content_type', 'object_id')

    field_name = models.CharField(max_length=256, null=True, blank=True)

    file_obj = models.FileField(_("file"), upload_to=upload_path)
    original_filename = models.CharField(_("original filename"), max_length=255, blank=True, null=True)

    # for internal use...

    owner = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        related_name='owned_%(class)ss', on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('owner'),
    )

    uuid = models.UUIDField()

    position = PositionField(_("order"), default=-1, collection=('object_id', 'content_type'))

    timestamp = models.DateTimeField(default=timezone.now)

    objects = AttachmentManager()

    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')
        unique_together = ['content_type', 'object_id', 'uuid']
        ordering = ['-timestamp', 'position']

    def __str__(self):
        if self.original_filename:
            return self.original_filename
        return str(self.file_obj.name)

    def get_absolute_url(self):
        return self.file_obj.url

    def as_file(self):
        class AttachmentFile(File):
            uuid = str(self.uuid)

        return AttachmentFile(self.file_obj, self.original_filename)

    def delete(self, *args, **kwargs):
        if self.file_obj and self.file_obj.storage.exists(self.file_obj.name):
            self.file_obj.delete()

        super(Attachment, self).delete(*args, **kwargs)


@python_2_unicode_compatible
class Temporary(models.Model):

    formid = models.CharField(max_length=128)

    attachments = GenericRelation(Attachment)

    # for internal use...

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta(object):
        verbose_name = _('temporary')
        verbose_name_plural = _('temporary')
        ordering = ['-timestamp']

    def __str__(self):
        return self.formid

    @property
    def is_expired(self):
        EXPIRY_AGE = settings.FINEUPLOADER_TEMPORARY_AGE

        if (self.timestamp + timedelta(seconds=EXPIRY_AGE)) <= timezone.localtime(timezone.now()):
            return True
        else:
            return False
