# -*- coding: utf-8 -*-

from django.conf import settings

SITE_SLUG = getattr(settings, 'SITE_SLUG', 'site')

WATCH_CHANNELS = getattr(settings, 'PRESENCE_WATCH_CHANNELS', [
                         SITE_SLUG + '_public'])
PUBLISH_CHANNEL = getattr(
    settings, 'PRESENCE_PUBLISH_CHANNEL', SITE_SLUG + '_presence')

FREQUENCY = getattr(settings, 'PRESENCE_FREQUENCY', 10)

TABS = getattr(settings, 'PRESENCE_TABS', False)
