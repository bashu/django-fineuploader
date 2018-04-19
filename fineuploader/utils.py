# -*- coding: utf-8 -*-

import uuid
import pathlib

from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import slugify as default_slugify

from .conf import settings

slugify = lambda x: default_slugify(x).lower().strip()

def parse_filename(filename):
    path = pathlib.Path(filename)

    return path.stem, path.suffix.lower()

def get_valid_filename(filename):
    stem, suffix = parse_filename(filename)

    return "{uuid}{suffix}".format(uuid=uuid.uuid4(), suffix=suffix)

def get_upload_model():
    try:
        return django_apps.get_model(settings.FINEUPLOADER_UPLOAD_MODEL)
    except ValueError:
        raise ImproperlyConfigured(
            'FINEUPLOADER_UPLOAD_MODEL must be of the form \'app_label.model_name\'')
    except LookupError:
        raise ImproperlyConfigured(
            'FINEUPLOADER_UPLOAD_MODEL refers to model \'%s\' that has not been installed' % settings.FINEUPLOADER_UPLOAD_MODEL)
