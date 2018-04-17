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

and include ``fineuploader`` templates

.. code-block:: html+django

    {% include "fineuploader/fineuploader_css.html" %} {# Before the closing head tag #}
    {% include "fineuploader/fineuploader_js.html" %} {# Before the closing body tag #}
    
Usage
-----

License
-------

``django-fineuploader`` is released under the BSD license.

.. _django: https://www.djangoproject.com/

.. _`Fine Uploader`: http://fineuploader.com
