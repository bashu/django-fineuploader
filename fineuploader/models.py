# -*- coding: utf-8 -*-

import os
import inspect
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import get_callable

from django.core.files import File
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import TemporaryManager
from .utils import slugify
from .conf import settings


def upload_path(instance, filename):
    FILENAME_FUNCTION = getattr(
        settings, 'FINEUPLOADER_FILENAME_FUNCTION', None)

    func = FILENAME_FUNCTION
    if func is None:
        func = lambda x: x

    if isinstance(func, str):
        func = get_callable(func)

    return os.path.join(
        slugify(instance.__name__) if inspect.isclass(instance) else slugify(instance.__class__.__name__),
        func(filename),
    )


@python_2_unicode_compatible
class Temporary(models.Model):

    formid = models.CharField(max_length=128)
    field_name = models.CharField(max_length=256, null=True, blank=True)

    file_obj = models.FileField(_("file"), max_length=255, upload_to=upload_path)
    original_filename = models.CharField(_("original filename"), max_length=255, blank=True, null=True)

    # for internal use...

    uuid = models.UUIDField()

    timestamp = models.DateTimeField(default=timezone.now)

    objects = TemporaryManager()

    class Meta(object):
        verbose_name = _('temporary upload')
        verbose_name_plural = _('temporary uploads')
        # Query string to get back existing uploaded file is using form_id and field_name
        index_together = (
            ('formid', 'field_name'),
        )
        ordering = ['-timestamp']

    def __str__(self):
        if self.original_filename not in ('', None):
            return self.original_filename
        else:
            return self.file_obj.name

    @property
    def is_expired(self):
        EXPIRY_AGE = settings.FINEUPLOADER_TEMPORARY_AGE

        if (self.created + timedelta(seconds=EXPIRY_AGE)) <= timezone.localtime(timezone.now()):
            return True
        else:
            return False

    def as_file(self):
        class TemporaryFile(File):
            uuid = str(self.uuid)

        return TemporaryFile(self.file_obj, self.original_filename)

    def delete(self, *args, **kwargs):
        if self.file_obj and self.file_obj.storage.exists(self.file_obj.name):
            self.file_obj.delete()

        super(Temporary, self).delete(*args, **kwargs)
