# -*- coding: utf-8 -*-

import logging

from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.urlresolvers import get_callable
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType

from attachments.models import Attachment

from .ajaxuploader.backends import local as backend
from .models import Temporary
from .conf import settings

logger = logging.getLogger(__name__)


def get_target_object(request, context):
    obj = ContentType.objects.get_for_id(
        context['content_type']).get_object_for_this_type(pk=context['object_id'])

    if isinstance(obj, Temporary):
        return obj

    # TODO: check for permissions ?

    return obj


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

        try:
            target_object = self.get_target_object(request, request.POST)

            model_info = {
                'creator': request.user,
                'content_type': ContentType.objects.get_for_model(target_object.__class__),
                'object_id': target_object.pk,
            }

            a = Attachment(attachment_file=None, **model_info)

            with open(self._path) as fh:
                a.attachment_file.save(original_filename, ContentFile(fh.read()), save=True)
            a.save()

            response.update({'newUuid': a.pk})

        except Exception, e:
            return self.failure(unicode(e), request)

        response.update({
            'content_type': request.POST['content_type'],
            'object_id': request.POST['object_id'],
        })

        return response

    def get_target_object(self, request, context):
        return get_target_object(request, context)
