# -*- coding: utf-8 -*-

from django.db import models
try:
  from django.core.urlresolvers import reverse
except ModuleNotFoundError:
  from django.urls import reverse


class ExampleModel(models.Model):

    def get_absolute_url(self):
        return reverse('example_edit', kwargs={'pk': self.pk})

