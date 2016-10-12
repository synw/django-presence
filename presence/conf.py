# -*- coding: utf-8 -*-

from django.conf import settings


ASYNC_BACKEND =  getattr(settings, 'PRESENCE_ASYNC_BACKEND', 'celery')

SITE_SLUG =  getattr(settings, 'SITE_SLUG', 'site')
CHANNEL = getattr(settings, 'PRESENCE_CHANNEL', SITE_SLUG+'_public')

GLOBAL_WORKER = getattr(settings, 'PRESENCE_GLOBAL_WORKER', False)

FREQUENCY = getattr(settings, 'PRESENCE_FREQUENCY', 10)