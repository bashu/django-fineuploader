# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType

from positions.managers import PositionManager, PositionQuerySet


class AttachmentQuerySet(PositionQuerySet):

    def for_model(self, model):
        return self.filter(
            content_type=ContentType.objects.get_for_model(model))

    def for_object(self, obj, field_name=None):
        queryset = self.for_model(obj.__class__).filter(object_id=obj.pk)
        if field_name:
            queryset = queryset.filter(field_name=field_name)
        return queryset


class AttachmentManager(PositionManager):

    def get_queryset(self):
        return AttachmentQuerySet(
            self.model, position_field_name=self.position_field_name)

    def for_model(self, model):
        return self.get_queryset().for_model(model)

    def for_object(self, obj, field_name=None):
        return self.for_model(obj.__class__).for_object(obj, field_name=field_name)
