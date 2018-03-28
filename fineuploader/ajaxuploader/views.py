# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed

from .backends.local import LocalUploadBackend
from .signals import file_uploaded


class AjaxFileUploader(object):

    def __init__(self, backend=None, **kwargs):
        if backend is None:
            backend = LocalUploadBackend
        self.get_backend = lambda: backend(**kwargs)

    def __call__(self, request, *args, **kwargs):
        return self._ajax_upload(request, *args, **kwargs)

    def _ajax_upload(self, request, *args, **kwargs):
        if request.method == "POST":
            upload = request.FILES.get('qqfile', None)
            if not upload:
                return HttpResponseBadRequest("AJAX request not valid")

            filename = upload.name
            backend = self.get_backend()

            # custom filename handler
            filename = (backend.update_filename(request, filename, *args, **kwargs)
                        or filename)
            # save the file
            backend.setup(request, filename, *args, **kwargs)
            success = backend.upload(upload, filename, False, *args, **kwargs)

            # callback
            extra_context = backend.upload_complete(request, filename, uuid=request.POST['qquuid'], *args, **kwargs)

            if success is True:
                file_uploaded.send(sender=self.__class__, backend=backend, request=request, extra_context=extra_context)

            # let Ajax Upload know whether we saved it or not
            ret_json = {'success': success, 'filename': filename}
            if extra_context is not None:
                ret_json.update(extra_context)

            # although "application/json" is the correct content type, IE throws a fit
            return HttpResponse(json.dumps(ret_json, cls=DjangoJSONEncoder), content_type='text/html; charset=utf-8')
        else:
            response = HttpResponseNotAllowed(['POST'])
            response.write("ERROR: Only POST allowed")
            return response
