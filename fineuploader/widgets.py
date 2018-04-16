# -*- coding: utf-8 -*-

import json

from django.forms import ClearableFileInput

from .models import Temporary


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

    def value_from_datadict(self, data, files, name):
        files = super(FineInput, self).value_from_datadict(data, files, name)
        if bool(files) is True:  # suddenly files!
            return files

        formid = data.get(self.formid_field_name, None)
        if bool(formid) is True:
            return [
                t.as_file() for t in Temporary.objects.filter(
                    formid=formid, field_name=name)
            ]
        return None
