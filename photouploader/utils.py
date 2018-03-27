# -*- coding: utf-8 -*-

import uuid
import pathlib

from django.utils.text import slugify as default_slugify

slugify = lambda x: default_slugify(x).lower().strip()

def parse_filename(filename):
    path = pathlib.Path(filename)

    return path.stem, path.suffix.lower()

def get_valid_filename(filename):
    stem, suffix = parse_filename(filename)

    return "{uuid}{suffix}".format(uuid=uuid.uuid4(), suffix=suffix)
