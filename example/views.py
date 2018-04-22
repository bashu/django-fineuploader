# -*- coding: utf-8 -*-

from django import forms
from django.urls import reverse
from django.views import generic

from fineuploader.forms import FineFormMixin
from fineuploader.formfields import FineFileField

from .models import ExampleModel


class ExampleForm(FineFormMixin, forms.ModelForm):

    files = FineFileField(label="Files")

    class Meta:
        model = ExampleModel
        fields = ['files']
        
    def save(self, *args, **kwargs):
        obj = super(ExampleForm, self).save(commit=True)

        self.handle_upload(obj)  # handle uploaded files

        self.delete_temporary_files()  # deleting temporary files / objects

        return obj


class ExampleCreateView(generic.CreateView):
    template_name = 'upload.html'
    form_class = ExampleForm


class ExampleUpdateView(generic.UpdateView):
    template_name = 'upload.html'
    form_class = ExampleForm
    model = ExampleModel
