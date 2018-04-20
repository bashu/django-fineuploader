# -*- coding: utf-8 -*-

import uuid

from django import forms
from django.utils import six

from .formfields import FineFieldMixin
from .utils import get_upload_model
from .conf import settings


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

    def delete_temporary_files(self):
        formid = self.data.get(self.add_prefix(self.formid_field_name), self.initial.get(self.add_prefix(self.formid_field_name)))

        if bool(formid) is True:
            for field_name, f in six.iteritems(self.fields):
                if not issubclass(self.fields[field_name].__class__, FineFieldMixin):
                    continue

                for t in get_upload_model().objects.filter(
                        formid=formid, field_name=field_name):
                    t.delete()

    def handle_upload(self, *args, **kwargs):
        for f in self.fields:
            if not issubclass(self.fields[f].__class__, FineFieldMixin):
                continue

            for file_obj in self.cleaned_data[f]:
                self.save_file(file_obj, f, *args, **kwargs)

    def save_file(self, file_obj, field_name, *args, **kwargs):
        raise NotImplementedError
