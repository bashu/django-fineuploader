# -*- coding: utf-8 -*-

from django import forms
from django.urls import reverse
from django.views import generic

from fineuploader.forms import FineFormMixin
from fineuploader.formfields import FineFileField


class ExampleForm(FineFormMixin, forms.Form):
    input_file = FineFileField(label="Files")

    def save_file(self, file_obj, field_name, *args, **kwargs):
        pass


class ExampleView(generic.FormView):
    template_name = 'upload.html'
    form_class = ExampleForm

    def form_valid(self, form):
        form.handle_upload()

        self.success_url = reverse('existing_file_example', kwargs=dict(formid=str(self.request.POST.get(self.get_form_class().formid_field_name))))

        return super(ExampleView, self).form_valid(form)


class ExistingFileExampleView(ExampleView):
    template_name = 'upload.html'
    form_class = ExampleForm

    def get_form_kwargs(self):
        kwargs = super(ExistingFileExampleView, self).get_form_kwargs()
        kwargs['initial'].update({
            self.get_form_class().formid_field_name: self.kwargs['formid']
        })
        return kwargs
