# -*- coding: utf-8 -*-

from django.db import models


class UploadManager(models.Manager):

    def try_get(self, **kwargs):
        qs = self.get_queryset().filter(**kwargs)
        if qs.exists():
            return qs.get()
        else:
            return None
