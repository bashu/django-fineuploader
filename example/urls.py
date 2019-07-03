"""example URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import re

from django.conf.urls import url, include
from django.contrib import admin

from django.conf import settings

urlpatterns = [url(r"^admin/", admin.site.urls), url(r"^fineuploader/", include("fineuploader.urls"))]

if settings.SERVE_MEDIA:
    from django.views.static import serve

    urlpatterns += [
        url(
            r"^%s(?P<path>.*)$" % re.escape(settings.STATIC_URL.lstrip("/")),
            serve,
            kwargs={"document_root": settings.STATIC_ROOT},
        )
    ]

    urlpatterns += [
        url(
            r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
            serve,
            kwargs={"document_root": settings.MEDIA_ROOT},
        )
    ]

from .views import ExampleCreateView, ExampleUpdateView

urlpatterns += [
    url(r"^$", ExampleCreateView.as_view(), name="example_create"),
    url(r"^(?P<pk>[0-9a-f-]+)/$", ExampleUpdateView.as_view(), name="example_edit"),
]
