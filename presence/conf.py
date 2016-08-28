# -*- coding: utf-8 -*-

from django.conf import settings


ASYNC_BACKEND =  getattr(settings, 'PRESENCE_ASYNC_BACKEND', 'celery')