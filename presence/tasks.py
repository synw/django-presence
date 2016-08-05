# -*- coding: utf-8 -*-

import redis
from cent.core import Client
from django.conf import settings
from huey.contrib.djhuey import crontab, periodic_task
from instant import broadcast
from instant.conf import CENTRIFUGO_PORT, CENTRIFUGO_HOST, SECRET_KEY, REDIS_HOST, REDIS_PORT, REDIS_DB, SITE_SLUG
from instant.utils import _get_public_channel

DEBUG = False

@periodic_task(crontab(minute='*'))
def update_presence():
    """
    Fetch presence info every minute and post it to the clients for update.
    The info is saved into Redis to use for the initial http connection
    """
    # get presence info from Centrifugo
    cent_url = CENTRIFUGO_HOST+":"+str(CENTRIFUGO_PORT)
    client = Client(cent_url, SECRET_KEY, timeout=1)
    clients = client.presence(_get_public_channel())
    if DEBUG:
        print "Updating presence"
    # post presence info
    total_users = 0
    anonymous_users = 0
    users = []
    for client in clients.keys():
        total_users += 1
        user = clients[client]["user"]
        if user == "":
            anonymous_users += 1
        if DEBUG and user != "":
            print "Client: "+str(user)
        if user not in users and user != "":
            users.append(user.encode('utf8'))
    if DEBUG:
        print str(anonymous_users)+" anonymous users"
        print "Connected users:"
        for user in users:
            print '- '+user
    # update info in Redis for the http connections
    store = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    key = SITE_SLUG+'_num_anonymous'
    store.set(key, anonymous_users)
    key = SITE_SLUG+'_users'
    store.delete(key)
    if DEBUG:
        print str(key)+' / '+str(users)
    if len(users) > 0:
        store.lpush(key, *users)
    # send presence info into a Centrifugo channel
    msg = ",".join(users)+'/'+str(anonymous_users)
    if total_users > 0:
        broadcast(message=msg, event_class="__presence__")
    return