# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseNotAllowed

from .ajaxuploader.views import AjaxFileUploader
from .backends import FineUploadBackend, get_target_object
from .models import Attachment

request_endpoint = AjaxFileUploader(backend=FineUploadBackend)


# TODO: replace with class-based view
def session_endpoint(request, *args, **kwargs):
    if request.method == "GET":
        try:
            target_object = get_target_object(request, request.GET)
        except Exception, e:
            return HttpResponse(json.dumps(unicode(e), cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8", status=400)

        params = {
            'obj': target_object
        }

        if request.GET.get('field_name'):
            params['field_name'] = request.GET.get('field_name')
        
        response = []
        for a in Attachment.objects.for_object(**params):
            response.append({
                'name': str(a),
                'uuid': str(a.uuid),
                'size': a.file_obj.size,
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

        params = {
            'obj': target_object
        }

        if request.GET.get('field_name'):
            params['field_name'] = request.GET.get('field_name')

        try:
            Attachment.objects.for_object(**params).get(uuid=request.POST['qquuid']).delete()
        except ObjectDoesNotExist, e:
            raise Http404

        # although "application/json" is the correct content type, IE throws a fit
        return HttpResponse(json.dumps({'success': True}, cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8")
    else:
        return HttpResponseNotAllowed(['POST'])
