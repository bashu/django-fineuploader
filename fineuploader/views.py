# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseNotAllowed

from attachments.models import Attachment

from .ajaxuploader.views import AjaxFileUploader
from .backends import FineUploadBackend, get_target_object

request_endpoint = AjaxFileUploader(backend=FineUploadBackend)


# TODO: replace with class-based view
def session_endpoint(request, *args, **kwargs):
    if request.method == "GET":
        try:
            target_object = get_target_object(request, request.GET)
        except Exception, e:
            return HttpResponse(json.dumps(unicode(e), cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8", status=400)

        response = []
        for a in Attachment.objects.attachments_for_object(target_object):
            response.append({
                'name': a.filename,
                'uuid': a.pk,
                'size': a.attachment_file.size,
            })

        # although "application/json" is the correct content type, IE throws a fit
        return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8")
    else:
        return HttpResponseNotAllowed(['GET'])


# TODO: replace with class-based view
def delete_endpoint(request, *args, **kwargs):
    if request.method == "POST":
        try:
            target_object = get_target_object(request, request.POST)
        except Exception, e:
            return HttpResponse(json.dumps({unicode(e)}, cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8", status=400)

        try:
            Attachment.objects.attachments_for_object(target_object).get(
                pk=request.POST['qquuid']).delete()
        except ObjectDoesNotExist, e:
            raise Http404

        # although "application/json" is the correct content type, IE throws a fit
        return HttpResponse(json.dumps({'success': True}, cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8")
    else:
        return HttpResponseNotAllowed(['POST'])

