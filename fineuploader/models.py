# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.files import File
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _

from attachments.models import Attachment as AttachmentBase
from positions.fields import PositionField

from .conf import settings
from .managers import AttachmentManager


class Attachment(AttachmentBase):

    field_name = models.CharField(max_length=256, null=True, blank=True)

    original_filename = models.CharField(_("original filename"), max_length=255, blank=True, null=True)

    # for internal use...

    uuid = models.UUIDField()

    position = PositionField(_("order"), default=-1, collection=("object_id", "content_type"))

    objects = AttachmentManager()

    class Meta:
        verbose_name = _("attachment")
        verbose_name_plural = _("attachments")
        ordering = ["-created", "position"]

    def __str__(self):
        return _("{username} attached {filename}").format(
            username=self.creator.get_username(),
            filename=self.original_filename if self.original_filename else self.attachment_file.name,
        )

    def as_file(self):
        class AttachmentFile(File):
            uuid = str(self.uuid)

        return AttachmentFile(self.attachment_file, self.original_filename)


class Temporary(models.Model):

    formid = models.CharField(max_length=128)

    attachments = GenericRelation(Attachment)

    # for internal use...

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta(object):
        verbose_name = _("temporary")
        verbose_name_plural = _("temporary")
        ordering = ["-timestamp"]

    def __str__(self):
        return self.formid

    @property
    def is_expired(self):
        EXPIRY_AGE = settings.FINEUPLOADER_TEMPORARY_AGE

        if (self.timestamp + timedelta(seconds=EXPIRY_AGE)) <= timezone.localtime(timezone.now()):
            return True
        else:
            return False
