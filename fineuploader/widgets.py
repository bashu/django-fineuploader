# -*- coding: utf-8 -*-

import json

from django.forms import ClearableFileInput
from django.contrib.contenttypes.models import ContentType


class FineInput(ClearableFileInput):
    template_name = 'fineuploader/fineinput.html'
    target_object = None

    def __init__(self, file_limit=4, size_limit=10485760, attrs=None):
        self.file_limit, self.size_limit = file_limit, size_limit
        super(FineInput, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        target_object = self.target_object

        context = self.get_context(name, value, attrs)
        context['widget'].update({
            'options': {
                'fileLimit': self.file_limit,
                'sizeLimit': self.size_limit,
            },
            'content_type': ContentType.objects.get_for_model(target_object),
            'object': target_object,
        })
        return self._render(self.template_name, context, renderer)
