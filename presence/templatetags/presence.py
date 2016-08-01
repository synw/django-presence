# -*- coding: utf-8 -*-

import redis
from django import template
from django.conf import settings


REDIS_HOST = getattr(settings, 'MQUEUE_REDIS_HOST', 'localhost')
REDIS_PORT = getattr(settings, 'MQUEUE_REDIS_PORT', 6379)
REDIS_DB = getattr(settings, 'MQUEUE_REDIS_DB', 0)
SITE_SLUG =  getattr(settings, 'SITE_SLUG', 'site')

register = template.Library()

@register.simple_tag
def get_presence():
    store = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    key = SITE_SLUG+'_users'
    users = store.lrange(key, 0, -1)
    num_anonymous = store.get(SITE_SLUG+'_num_anonymous')
    return {'users':users, 'num_anonymous':num_anonymous}



