# -*- coding: utf-8 -*-

from datetime import timedelta
from django.conf import settings


ASYNC_BACKEND =  getattr(settings, 'ASYNC_BACKEND', 'celery')