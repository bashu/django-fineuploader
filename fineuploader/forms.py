# -*- coding: utf-8 -*-

import uuid

from django import forms
from django.utils import six

from .models import Temporary
from .formfields import FineFieldMixin


class FineFormMixin(object):
    formid_field_name = 'formid'
    request = None

    def __init__(self, *args, **kwargs):
        if 'prefix' in kwargs and kwargs['prefix'] is not None:
            self.prefix = kwargs['prefix']

        if kwargs.get('initial', None) is None:
            kwargs['initial'] = {}
        if not self.add_prefix(self.formid_field_name) in kwargs['initial']:
            kwargs['initial'].update({
                self.add_prefix(self.formid_field_name): str(uuid.uuid4())})
        super(FineFormMixin, self).__init__(*args, **kwargs)

        self.fields[self.formid_field_name] = forms.CharField(
            widget=forms.HiddenInput, initial=kwargs['initial'][self.add_prefix(self.formid_field_name)], required=False)

        formid = self.data.get(self.add_prefix(self.formid_field_name), self.initial.get(self.add_prefix(self.formid_field_name)))
        for f in self.fields:
            if not issubclass(self.fields[f].__class__, FineFieldMixin):
                continue
            
            self.fields[f].widget.formid_field_name = self.add_prefix(self.formid_field_name)

    def handle_uploads(self, *args, **kwargs):
        for f in self.fields:
            if not issubclass(self.fields[f].__class__, FineFieldMixin):
                continue

            for file_obj in self.cleaned_data[f]:
                self.save_file(file_obj, f, *args, **kwargs)

    def save_file(self, file_obj, field_name, *args, **kwargs):
        raise NotImplementedError
