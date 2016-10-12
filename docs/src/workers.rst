Workers
=======

The presence data is automaticaly updated from the time based worker asking Centrifugo who is on the socket. 
This data is broadcasted to the clients over the websocket.

Default worker
--------------

The default worker for presence updating is a go module. Install with the 
command ``python manage.py installpres``: it will generate two files in your main project directory:

- ``centpres``: the executable
- ``centpres_config.json``: the config file

To run the worker: ``./centpres``. This will start updating presence info.

Note: you can also compile the go module from the source in *presence/go/src/*

Alternate workers
-----------------

For those who want a more traditional way two python async backends are supported: Celery and Huey.

For Celery in settings.py:

.. highlight:: python

::
   
   PRESENCE_ASYNC_BACKEND = "celery"

   from datetime import timedelta
   CELERYBEAT_SCHEDULE = {
       'update-presence': {
           'task': 'presence.tasks.update_presence',
           'schedule': timedelta(seconds=30),
       },
   }

Then:

.. highlight:: bash

::
   
   celery -A project_name beat  -l info --broker='redis://localhost:6379/0'
   celery -A project_name worker  -l info --broker='redis://localhost:6379/0'
   # or whatever broker or settings

For Huey in settings.py:

.. highlight:: python

::
   
   PRESENCE_ASYNC_BACKEND = "huey"
   
   from huey import RedisHuey
   HUEY = RedisHuey('your_project_name')

Then:

.. highlight:: bash

::
   
   python manage.py run_huey
   
Note: Huey is limited: it will update presence info every minute