# -*- coding: utf-8 -*-

from django.conf import settings  # pylint: disable=W0611

from appconf import AppConf


class PhotoUploaderSettings(AppConf):
    THUMBNAIL_SIZE = 72
    FILENAME_FUNCTION = 'photouploader.utils.get_valid_filename'
    TEMPORARY_AGE = 60 * 60 * 24 * 7  # default is one week

    class Meta:
        prefix = 'photouploader'
