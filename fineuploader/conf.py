# -*- coding: utf-8 -*-

from django.conf import settings  # noqa

from appconf import AppConf


class FineUploaderSettings(AppConf):
    TEMPORARY_AGE = 60 * 60 * 24 * 7  # default is one week

    class Meta:
        prefix = 'fineuploader'
