django-fineuploader
===================

This is a Django_ integration of `Fine Uploader`_ JavaScript Upload Library.

.. image:: https://img.shields.io/pypi/v/django-fineuploader.svg
    :target: https://pypi.python.org/pypi/django-fineuploader/

.. image:: https://img.shields.io/pypi/dm/django-fineuploader.svg
    :target: https://pypi.python.org/pypi/django-fineuploader/

.. image:: https://img.shields.io/github/license/bashu/django-fineuploader.svg
    :target: https://pypi.python.org/pypi/django-fineuploader/

Installation
------------

.. code-block:: shell

    pip install django-fineuploader
    
External dependencies
~~~~~~~~~~~~~~~~~~~~~

* jQuery - This is not included in the package since it is expected that in most scenarios this would already be available.

Setup
-----

Add ``fineuploader`` and ``fineuploader.ajaxuploader`` to  ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS += (
        'fineuploader',
        'fineuploader.ajaxuploader',
    )

Be sure you have the ``django.template.context_processors.request`` processor

.. code-block:: python

    TEMPLATES = [
        {
            ...
            'OPTIONS': {
                'context_processors': [
                    ...
                    'django.template.context_processors.request',
                ],
            },
        },
    ]

Update your ``urls.py`` file:

.. code-block:: python

    urlpatterns += [
        url(r'^fineuploader/', include('fineuploader.urls')),
    ]
    
and include ``fineuploader`` templates

.. code-block:: html+django

    {% include "fineuploader/fineuploader_css.html" %} {# Before the closing head tag #}
    {% include "fineuploader/fineuploader_js.html" %} {# Before the closing body tag #}
    
When deploying on production server, don't forget to run:

.. code-block:: shell

    python manage.py collectstatic

Usage
-----

.. code-block:: python

    # forms.py

    from django import forms

    from fineuploader.forms import FineFormMixin
    from fineuploader.formfields import FineFileField

    class ExampleForm(FineFormMixin, forms.ModelForm):

        files = FineFileField(label="Files")

        class Meta:
            ...

        def save(self, *args, **kwargs):
            obj = super(ExampleForm, self).save(commit=True)

            self.handle_upload(obj, self.request)  # handle uploaded files

            self.delete_temporary_files()  # deleting temporary files / objects

            return obj

    # views.py

    from django.views import generic
    from django.contrib.auth.mixins import LoginRequiredMixin

    class ExampleCreateView(LoginRequiredMixin, generic.CreateView):
        form_class = ExampleForm  # our custom form class
        ...

        def get_form_kwargs(self):
            kwargs = super(ExampleCreateView, self).get_form_kwargs()
            kwargs.update({"request": self.request})  # must pass self.request into form
            return kwargs

    class ExampleUpdateView(LoginRequiredMixin, generic.UpdateView):
        form_class = ExampleForm  # our custom form class
        ...
        
        def get_form_kwargs(self):
            kwargs = super(ExampleUpdateView, self).get_form_kwargs()
            kwargs.update({"request": self.request})  # must pass self.request into form
            return kwargs

License
-------

``django-fineuploader`` is released under the BSD license.

.. _django: https://www.djangoproject.com/

.. _`Fine Uploader`: http://fineuploader.com
