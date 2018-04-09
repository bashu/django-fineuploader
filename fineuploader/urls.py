# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^request/$', views.request_endpoint, name="request_endpoint"),
    url(r'^session/$', views.session_endpoint, name="session_endpoint"),
    url(r'^delete/$', views.delete_endpoint, name="delete_endpoint"),
]
