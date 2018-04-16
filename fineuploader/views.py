# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, HttpResponseNotAllowed

from .ajaxuploader.views import AjaxFileUploader
from .backends import FineUploadBackend
from .models import Temporary

request_endpoint = AjaxFileUploader(backend=FineUploadBackend)


# TODO: replace with class-based view
def session_endpoint(request, *args, **kwargs):
    if request.method == "GET":
        params = {
            'formid': request.GET['formid'],
        }

        if request.GET.get('field_name'):
            params['field_name'] = request.GET.get('field_name')
        
        response = []
        for t in Temporary.objects.filter(**params).order_by('timestamp'):
            response.append({
                'name': unicode(t),
                'uuid': str(t.uuid),
                'size': t.file_obj.size,
            })

        # although "application/json" is the correct content type, IE throws a fit
        return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8")
    else:
        return HttpResponseNotAllowed(['GET'])


# TODO: replace with class-based view
def delete_endpoint(request, *args, **kwargs):
    if request.method == "POST":
        try:
            Temporary.objects.get(uuid=request.POST['qquuid']).delete()
        except ObjectDoesNotExist, e:
            raise Http404

        # although "application/json" is the correct content type, IE throws a fit
        return HttpResponse(json.dumps({'success': True}, cls=DjangoJSONEncoder), content_type="text/html; charset=utf-8")
    else:
        return HttpResponseNotAllowed(['POST'])
