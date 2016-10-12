# -*- coding: utf-8 -*-

import os
from cent.core import Client
from instant.producers import broadcast
from instant.conf import CENTRIFUGO_PORT, CENTRIFUGO_HOST, SECRET_KEY
from presence.conf import ASYNC_BACKEND, CHANNEL, GLOBAL_WORKER
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
    clients = client.presence(CHANNEL)
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

def global_update():
    com = './presence/go/centpres'
    os.system(com)
    return

if ASYNC_BACKEND == 'huey':

    @periodic_task(crontab(minute='*'))
    def update_presence():
        if GLOBAL_WORKER is True:
            global_update()
        else:
            _update_presence()
        return

elif ASYNC_BACKEND == 'celery':
    
    @task(ignore_results=True)
    def update_presence():
        if GLOBAL_WORKER is True:
            global_update()
        else:
            _update_presence()
        return