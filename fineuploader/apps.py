# -*- coding: utf-8 -*-

from django.apps import AppConfig as DefaultAppConfig


class AppConfig(DefaultAppConfig):
    name = 'fineuploader'

    def ready(self):
        # Ensure everything below is only ever run once
        if getattr(AppConfig, 'has_run_ready', False):
            return
        AppConfig.has_run_ready = True
