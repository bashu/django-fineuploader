# -*- coding: utf-8 -*-

import uuid

from django import forms
from django.contrib.contenttypes.models import ContentType

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

    def handle_uploads(self, target_object, *args, **kwargs):
        for f in self.fields:
            if not isinstance(self.fields[f], FineFileField):
                continue

            for a in self.cleaned_data[f]:
                self.save_attachment(target_object, a, f, *args, **kwargs)

    def save_attachment(self, target_object, attachment, field_name, *args, **kwargs):
        attachment.content_type_id = ContentType.objects.get_for_model(
            target_object).pk
        attachment.object_id = target_object.pk
        attachment.save()

        return attachment
