# -*- coding: utf-8 -*-

from django import forms
from django.urls import reverse
from django.core import validators
from django.core.exceptions import ValidationError

from .widgets import FineInput


class FineFieldMixin(object):
    file_limit, size_limit = 4, 10485760  # 4 files by 10Mb
    widget = FineInput

    # TODO: configurable endpoints

    def __init__(self, *args, **kwargs):
        if 'file_limit' in kwargs:
            self.file_limit = kwargs.pop('file_limit')
        if 'size_limit' in kwargs:
            self.file_limit = kwargs.pop('size_limit')
        super(FineFieldMixin, self).__init__(*args, **kwargs)

        self.widget.file_limit = self.file_limit
        self.widget.size_limit = self.size_limit
    
    def run_validators(self, value):
        if value in self.empty_values:
            return
        errors = []
        for v in self.validators:
            try:
                if isinstance(value, list):
                    for vv in value:
                        v(vv)
                else:
                    v(value)
            except ValidationError as e:
                if hasattr(e, 'code') and e.code in self.error_messages:
                    e.message = self.error_messages[e.code]
                errors.extend(e.error_list)
        if errors:
            raise ValidationError(errors)

    def widget_attrs(self, widget):
        attrs = super(FineFieldMixin, self).widget_attrs(widget)

        attrs['multiple'] = 'multiple'
        return attrs

    def to_python(self, data):
        if data in validators.EMPTY_VALUES:
            return None
        elif isinstance(data, list):
            return [
                super(FineFieldMixin, self).to_python(f) for f in data
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


class FineFileField(FineFieldMixin, forms.FileField):
    pass


class FineImageField(FineFieldMixin, forms.ImageField):

    def widget_attrs(self, widget):
        attrs = super(FineImageField, self).widget_attrs(widget)

        if isinstance(widget, FineInput) and 'accept' not in widget.attrs:
            attrs.setdefault('accept', 'image/*')
        return attrs
