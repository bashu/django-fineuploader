# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation

from django.utils.translation import ugettext_lazy as _

from attachments.models import Attachment

from .managers import TemporaryManager
from .conf import settings


class Temporary(models.Model):

    formid = models.CharField(max_length=128)
    field_name = models.CharField(max_length=256, null=True, blank=True)

    attachments = GenericRelation(Attachment)

    # for internal use...

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

    @property
    def is_expired(self):
        EXPIRY_AGE = settings.FINEUPLOADER_TEMPORARY_AGE

        if (self.created + timedelta(seconds=EXPIRY_AGE)) <= timezone.localtime(timezone.now()):
            return True
        else:
            return False
