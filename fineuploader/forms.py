# -*- coding: utf-8 -*-

import uuid

from django import forms
from django.utils import six
from django.core.files import File

from attachments.models import Attachment

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
            
            self.fields[f].widget.target_object = self.get_target_object(formid, f)

    def _as_file(self, attachment):
        class AttachmentFile(File):
            content_type = attachment.content_type,
            object_id = attachment.pk
        
        return AttachmentFile(attachment.attachment_file, attachment.filename)

    def get_target_object(self, formid=None, field_name=None):
        if hasattr(self, 'instance') is True:
            if getattr(self.instance, 'pk', False):
                return self.instance

        # instance not found, trying to get temporary object...
        if formid and field_name:
            t, created = Temporary.objects.get_or_create(
                formid=formid, field_name=field_name)

            return t

        raise NotImplementedError

    def full_clean(self):
        if not self.is_bound:
            super(FineFormMixin, self).full_clean()
        else:
            formid = self.data.get(self.formid_field_name, self.initial.get(self.formid_field_name))
            for field_name, f in six.iteritems(self.fields):
                if not isinstance(self.fields[field_name], FineFileField):
                    continue
                target_object = self.get_target_object(formid, field_name)

                self.files[field_name] = [
                    self._as_file(a) for a in Attachment.objects.attachments_for_object(target_object)
                ]

            super(FineFormMixin, self).full_clean()

    def handle_uploads(self, *args, **kwargs):
        for f in self.fields:
            if not isinstance(self.fields[f], FineFileField):
                continue
            
            for file_obj in self.cleaned_data[f]:
                self.save_file(file_obj, f, *args, **kwargs)

    def save_file(self, file_obj, field_name, *args, **kwargs):
        raise NotImplementedError
