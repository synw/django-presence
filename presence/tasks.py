# -*- coding: utf-8 -*-

from cent.core import Client
from instant import broadcast
from instant.conf import CENTRIFUGO_PORT, CENTRIFUGO_HOST, SECRET_KEY, SITE_SLUG
from instant.utils import _get_public_channel
from presence.conf import ASYNC_BACKEND
if ASYNC_BACKEND == 'celery':
    from celery import task
elif ASYNC_BACKEND == 'huey':
    from huey.contrib.djhuey import crontab, periodic_task

DEBUG = False

def _update_presence():
    """
    Fetch presence info every minute from Centrifugo and post it to the clients for update.
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
    # send presence info into a Centrifugo channel
    msg = ",".join(users)+'/'+str(anonymous_users)
    if total_users > 0:
        broadcast(message=msg, event_class="__presence__")
    return

if ASYNC_BACKEND == 'huey':

    @periodic_task(crontab(minute='*'))
    def update_presence():
        return _update_presence()

elif ASYNC_BACKEND == 'celery':

    @task(ignore_results=True)
    def update_presence():
        return _update_presence()

