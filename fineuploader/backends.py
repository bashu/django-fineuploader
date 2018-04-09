# -*- coding: utf-8 -*-

import logging

from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.urlresolvers import get_callable

from .ajaxuploader.backends import local as backend
from .models import Temporary
from .conf import settings

logger = logging.getLogger(__name__)


class LocalUploadBackend(backend.LocalUploadBackend):
    FILENAME_FUNCTION = getattr(
        settings, 'FINEUPLOADER_FILENAME_FUNCTION', None)

    def setup(self, request, filename, *args, **kwargs):
        super(LocalUploadBackend, self).setup(
            request, filename, *args, **kwargs)
        self.request = request  # save request for a later use

    def upload_complete(self, request, filename, *args, **kwargs):
        try:
            response = super(LocalUploadBackend, self).upload_complete(
                request, filename, *args, **kwargs)
        except Exception, e:
            return self.failure(unicode(e), request)

        return response

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

        value = super(LocalUploadBackend, self).update_filename(
            request, func(filename), *args, **kwargs)
        return value

    def upload(self, uploaded, filename, raw_data, *args, **kwargs):
        success = super(LocalUploadBackend, self).upload(
            uploaded, filename, raw_data, *args, **kwargs)
        if success is False:
            self.log_exception("Failed to upload: %s" % filename, self.request)
        return success

    def log_exception(self, msg, request):
        logger.error(msg, exc_info=True, extra={'stack': True})


class FineUploadBackend(LocalUploadBackend):

    def upload_complete(self, request, filename, *args, **kwargs):
        response = super(FineUploadBackend, self).upload_complete(
            request, filename, *args, **kwargs)

        if request.POST.get('qqfilename'):
            original_filename = request.POST['qqfilename']
        else:
            original_filename = request.FILES['qqfile'].name

        model_info = {
            'uuid': request.POST['qquuid'],
            'formid': request.POST['formid'],
            'original_filename': original_filename,
            'timestamp': timezone.localtime(timezone.now()),
        }

        field_name = request.POST.get('field_name')
        if field_name:
            model_info['field_name'] = field_name

        t = Temporary(**model_info)

        with open(self._path) as fh:
            t.file_obj.save(filename, ContentFile(fh.read()), save=True)

        t.save()

        return response
