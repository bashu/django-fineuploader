# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse


class ExampleModel(models.Model):

    def get_absolute_url(self):
        return reverse('example_edit', kwargs={'pk': self.pk})

