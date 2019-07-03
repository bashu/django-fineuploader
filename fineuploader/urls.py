# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r"^request/$", login_required(views.request_endpoint), name="request_endpoint"),
    url(r"^session/$", login_required(views.session_endpoint), name="session_endpoint"),
    url(r"^delete/$", login_required(views.delete_endpoint), name="delete_endpoint"),
]
