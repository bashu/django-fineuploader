# -*- coding: utf-8 -*-

import uuid

from django import forms
from django.utils import six

from .models import Temporary
from .formfields import FineFileField


class FineFormMixin(object):
    formid_field_name = 'formid'
    request = None

    def __init__(self, *args, **kwargs):
        if kwargs.get('initial', None) is None:
            kwargs['initial'] = {}
        if not self.formid_field_name in kwargs['initial']:
            kwargs['initial'].update({
                self.formid_field_name: str(uuid.uuid4())})
        super(FineFormMixin, self).__init__(*args, **kwargs)

        self.fields[self.formid_field_name] = forms.CharField(
            widget=forms.HiddenInput, initial=kwargs['initial'][self.formid_field_name], required=False)

        formid = self.data.get(self.formid_field_name, self.initial.get(self.formid_field_name))
        for f in self.fields:
            if not isinstance(self.fields[f], FineFileField):
                continue
            
            self.fields[f].formid_field_name = self.formid_field_name

    def handle_uploads(self, *args, **kwargs):
        for f in self.fields:
            if not isinstance(self.fields[f], FineFileField):
                continue

            for file_obj in self.cleaned_data[f]:
                self.save_file(file_obj, f, *args, **kwargs)

    def save_file(self, file_obj, field_name, *args, **kwargs):
        raise NotImplementedError
