# -*- coding: utf-8 -*-

import os
import logging

from django.core.urlresolvers import get_callable

from easy_thumbnails.files import get_thumbnailer

from .ajaxuploader.backends import local as backend
from .conf import settings

logger = logging.getLogger(__name__)


class UploadBackend(backend.LocalUploadBackend):
    DIMENSIONS = (
        settings.PHOTOUPLOADER_THUMBNAIL_SIZE,
        settings.PHOTOUPLOADER_THUMBNAIL_SIZE
    )
    FILENAME_FUNCTION = getattr(
        settings, 'PHOTOUPLOADER_FILENAME_FUNCTION', None)
    KEEP_ORIGINAL = False
    UPSCALE = True
    CROP = True

    def setup(self, request, filename, *args, **kwargs):
        super(UploadBackend, self).setup(
            request, filename, *args, **kwargs)
        self.request = request  # save request for a later use

    def upload_complete(self, request, filename, *args, **kwargs):
        self._dest.close()  # close file descriptor

        try:
            thumb = self.generate_thumbnail(filename)

        except Exception, e:
            return self.failure(unicode(e), request)

        return {'thumbnailUrl': thumb.url}

    def failure(self, msg, request):
        self.log_exception(msg, request)
        return {'success': False, 'error': msg, 'preventRetry': True}

    def update_filename(self, request, filename, *args, **kwargs):
        # use custom photo filename function if any
        func = self.FILENAME_FUNCTION
        if func is None:
            func = lambda x: x

        # find callable by string
        if isinstance(func, str):
            func = get_callable(func)

        value = super(UploadBackend, self).update_filename(
            request, func(filename), *args, **kwargs)
        return value

    def upload(self, uploaded, filename, raw_data, *args, **kwargs):
        success = super(UploadBackend, self).upload(
            uploaded, filename, raw_data, *args, **kwargs)
        if success is False:
            self.log_exception("Failed to upload: %s" % filename, self.request)
        return success

    def generate_thumbnail(self, filename):
        with open(self._path) as fh:
            tt = get_thumbnailer(
                fh, os.path.join(self.UPLOAD_DIR, filename))

            return tt.get_thumbnail({
                'size': self.DIMENSIONS,
                'crop': self.CROP,
                'upscale': self.UPSCALE}, save=True)

    def log_exception(self, msg, request):
        logger.error(msg, exc_info=True, extra={'stack': True})
