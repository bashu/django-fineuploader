# -*- coding: utf-8 -*-

import uuid

from django import forms
from django.utils import six
from django.contrib.contenttypes.models import ContentType

from .formfields import FineFieldMixin
from .models import Attachment, Temporary
from .conf import settings


class FineFormMixin(object):
    formid_field_name = 'formid'

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

            self.fields[f].widget.target_object = self.get_target_object(formid, f)

    def get_target_object(self, formid=None, field_name=None):
        if hasattr(self, 'instance') is True:
            if getattr(self.instance, 'pk', False):
                return self.instance

        # instance not found, trying to get temporary object...
        if formid and field_name:
            t, created = Temporary.objects.get_or_create(formid=formid)

            return t

        raise NotImplementedError  # something unexpected ?

    def delete_temporary_files(self):
        formid = self.data.get(self.add_prefix(self.formid_field_name), self.initial.get(self.add_prefix(self.formid_field_name)))

        if bool(formid) is True:
            for field_name, f in six.iteritems(self.fields):
                if not issubclass(self.fields[field_name].__class__, FineFieldMixin):
                    continue

                for t in Temporary.objects.filter(formid=formid):
                    for a in t.attachments.filter(field_name=field_name):
                        a.delete()
                    t.delete()

    def handle_upload(self, target_object, request=None, *args, **kwargs):
        for f in self.fields:
            if not issubclass(self.fields[f].__class__, FineFieldMixin):
                continue

            for file_obj in self.cleaned_data[f]:
                self.save_attachment(target_object, file_obj, f, request,*args, **kwargs)

    def save_attachment(self, target_object, file_obj, field_name, request, *args, **kwargs):
        model_info = {
            'original_filename': file_obj.name,
            'owner': request.user if request and request.user.is_authenticated else None,
        }
            
        if field_name:
            model_info['field_name'] = field_name

        attachment, created = Attachment.objects.update_or_create(
            uuid=file_obj.uuid,
            content_type_id=ContentType.objects.get_for_model(target_object).pk,
            object_id=str(target_object.pk),
            defaults=model_info,
        )
        if created is True:
            attachment.file_obj.save(file_obj.name, file_obj, save=False)
        attachment.save()
