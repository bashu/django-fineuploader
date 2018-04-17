# -*- coding: utf-8 -*-

from django import forms
from django.urls import reverse
from django.core import validators

from .widgets import FineInput


class FineFileField(forms.FileField):
    file_limit, size_limit = 4, 10485760  # 4 files by 10Mb
    widget = FineInput

    # TODO: configurable endpoints

    def __init__(self, *args, **kwargs):
        if 'file_limit' in kwargs:
            self.file_limit = kwargs.pop('file_limit')
        if 'size_limit' in kwargs:
            self.file_limit = kwargs.pop('size_limit')
        super(FineFileField, self).__init__(*args, **kwargs)

        self.widget.file_limit = self.file_limit
        self.widget.size_limit = self.size_limit

    def widget_attrs(self, widget):
        attrs = super(FineFileField, self).widget_attrs(widget)

        attrs['multiple'] = 'multiple'
        return attrs

    def to_python(self, data):
        if data in validators.EMPTY_VALUES:
            return None
        elif isinstance(data, list):
            return [
                super(FineFileField, self).to_python(f) for f in data
            ]
        else:
            return [data]

    def bound_data(self, data, initial):
        result = []

        if initial:
            result += initial if isinstance(initial, list) else [initial]

        if data:
            result += data if isinstance(data, list) else [data]

        return result
