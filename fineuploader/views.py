# -*- coding: utf-8 -*-

from .ajaxuploader.views import AjaxFileUploader
from .backends import LocalUploadBackend


class FineUploaderView(AjaxFileUploader):

    def __init__(self, backend=None, **kwargs):
        if backend is None:
            backend = LocalUploadBackend
        self.get_backend = lambda: backend(**kwargs)
