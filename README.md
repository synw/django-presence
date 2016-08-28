# Django Presence

A widget to real time update a list of users present on the site. This package provides a javascript Centrifugo client
that listens to a websocket channel, and an async time based worker that updates the presence information.

## Install

Dependencies:

- [Centrifugo](https://github.com/centrifugal/centrifugo/) for the websocket server.
- [Django Instant](https://github.com/synw/django-instant) for the Centrifugo/Django layer.

Clone the repository

Set up Centrifugo and Django Instant:
 [instructions here](http://django-instant.readthedocs.io/en/latest/src/install.html)

## Configuration

Configure Centrifugo to handle presence info in the Centrifugo ``config.json``:

  ```javascript
{
	"secret": "70b651f6-775a-4949-982b-b387b31c1d84",
	"anonymous": true,
	"presence":true
}
  ```

In INSTALLED_APPS:

   ```python
"instant",
"presence",
  ```
  
In settings.py

   ```python
SITE_SLUG = "mysitename"
  ```
  
Choose an async worker: either the go module or a python backend.

#### Python async workers

Supported backends are Celery and Huey

##### Celery

Install Celery:

  ```bash
sudo apt-get install redis-server # example for debian
pip install redis celery
  ```
  
In settings.py:

  ```python
PRESENCE_ASYNC_BACKEND = "celery"

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'update-presence': {
        'task': 'presence.tasks.update_presence',
        'schedule': timedelta(minutes=1),
    },
}
  ```
You will need a ``celery.py`` file as explained 
[here](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)

##### Huey

  ```bash
sudo apt-get install redis-server # example for debian
pip install redis huey
  ```

In INSTALLED_APPS:
  
   ```python
"huey.contrib.djhuey",
  ```
  
In settings.py:

  ```python
PRESENCE_ASYNC_BACKEND = "huey"
from huey import RedisHuey
HUEY = RedisHuey('your_project_name')
  ```

#### Go async worker

Edit ``presence/go/config.json`` with the same Centrifugo settings that are in settings.py:

  ```javascript
{
	"centrifugo_secret_key":"70b651f6-775a-4949-982b-b387b31c1d84",
	"centrifugo_host":"localhost",
	"centrifugo_port":"8001",
	"channels":["SITESLUG_public"],
	"interval":"10s"
}
  ```
Replace SITESLUG with the value SITE_SLUG set in settings.py 

Interval is the update rate: ex: set to "1m" for one minute, to "30s" for 30 seconds 

The default async backend is the Go module, but you can chose the one you want:

- Celery: good if you are familiar with it and already using it
- Huey: easier to setup than Celery but limited
- Go: fast and nothing to install 

## Run the worker

[Run the Centrifugo server](http://django-instant.readthedocs.io/en/latest/src/usage.html)

#### Python workers

Run Redis and launch a Celery beat and a worker or a just a Huey worker:

  ```bash
celery -A project_name beat  -l info --broker='redis://localhost:6379/0'
celery -A project_name worker  -l info --broker='redis://localhost:6379/0'

# or
python manage.py run_huey
  ```

#### Go worker

Run the worker:

  ```bash
cd presence/go/
./centpres 
  ```

## Templates

Add a ``instant/extra_clients.js`` template with this content:

   ```django
{% include "presence/js/client.js" %}
  ```
  
Add a ``instant/extra_handlers.js`` template with this content:

   ```django
{% include "presence/js/handlers.js" %}
  ```
  
Where you want the presence widget to be place `{% include "presence/widget.html" %}`.

You can tweak ``presence/js/handlers.js`` to add your own client-side event handlers.

## How it works

The presence data is automaticaly updated from the time based worker asking Centrifugo who is on the socket. 
This data is broadcasted to the clients via the websocket.

In this design the server only pushes presence information. There are no requests made from actions on the
client side: for example it could be possible to fetch fresh info on each client connection, 
but it could lead to some unecessary ressources consumption, overloading scenarios or scaling problems. 

You can set this default update time to a lower value in the settings if you use the go worker or Celery.
Only Huey is limited to 1 minute.

