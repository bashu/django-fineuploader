# -*- coding: utf-8 -*-

import json

from django.forms import ClearableFileInput


class FineInput(ClearableFileInput):
    template_name = 'fineuploader/fineinput.html'

    def __init__(self, file_limit=4, size_limit=10485760, attrs=None):
        self.file_limit, self.size_limit = file_limit, size_limit
        super(FineInput, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        formid_field_name = self.formid_field_name

        context = self.get_context(name, value, attrs)
        context['widget'].update({
            'formid_field_name': formid_field_name,
            'options': {
                'fileLimit': self.file_limit,
                'sizeLimit': self.size_limit,
            },
        })
        return self._render(self.template_name, context, renderer)
