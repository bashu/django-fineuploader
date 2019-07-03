# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType

from positions.managers import PositionManager, PositionQuerySet


class AttachmentQuerySet(PositionQuerySet):

    def attachments_for_object(self, obj, field_name=None):
        object_type = ContentType.objects.get_for_model(obj)
        queryset = self.filter(content_type__pk=object_type.id, object_id=obj.pk)
        if field_name:
            queryset = queryset.filter(field_name=field_name)
        return queryset


class AttachmentManager(PositionManager):

    def get_queryset(self):
        return AttachmentQuerySet(
            self.model, position_field_name=self.position_field_name)

    def attachments_for_object(self, obj, field_name=None):
        return self.get_queryset().attachments_for_object(obj, field_name=field_name)
