# -*- coding: utf-8 -*-

import logging

from .ajaxuploader.views import AjaxFileUploader
from .backends import FineUploadBackend

logger = logging.getLogger(__name__)

request_endpoint = AjaxFileUploader(backend=FineUploadBackend)
