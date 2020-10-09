# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from fineuploader.formfields import FineFileField
from fineuploader.forms import FineFormMixin

from .models import ExampleModel


class ExampleForm(FineFormMixin, forms.ModelForm):

    files = FineFileField(label="Files")

    class Meta:
        model = ExampleModel
        fields = ["files"]

    def save(self, *args, **kwargs):
        obj = super(ExampleForm, self).save(commit=True)

        self.handle_upload(obj, self.request)  # handle uploaded files

        self.delete_temporary_files()  # deleting temporary files / objects

        return obj


class FormKwargsRequestMixin(object):
    def get_form_kwargs(self):
        kwargs = super(FormKwargsRequestMixin, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs


class ExampleCreateView(LoginRequiredMixin, FormKwargsRequestMixin, generic.CreateView):
    template_name = "upload.html"
    form_class = ExampleForm


class ExampleUpdateView(LoginRequiredMixin, FormKwargsRequestMixin, generic.UpdateView):
    template_name = "upload.html"
    form_class = ExampleForm
    model = ExampleModel
