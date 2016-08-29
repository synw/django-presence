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

# optional : if not set default is SITE_SLUG+'_public'
PRESENCE_CHANNEL = "mychannel"
  ```

#### Async backends

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
        'schedule': timedelta(seconds=30),
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

#### Global worker

You can update presence channels for multiple sites using one process. The standard python worker updates one channel.
A go worker is used to update multiple channels.

Create a ``centpres_config.json`` file either in your main django project directory or in ``~/.centpres`` or in
``/etc/centpres``
Use the same Centrifugo settings that are in settings.py and provide a list of channels to push presence updates to:

  ```javascript
{
	"centrifugo_secret_key":"70b651f6-775a-4949-982b-b387b31c1d84",
	"centrifugo_host":"localhost",
	"centrifugo_port":"8001",
	"channels":["channel1", "channel2", "channel3", "channel4", "channel5", "channel6"]
}
  ```
  
Option 1 is to set a cronjob on ``presence/go/centpres``, and you don't need any async backend.
Option 2 is to use the async backend to trigger the updates: in settings.py: ``PRESENCE_GLOBAL_WORKER = True``

The default async backend is Celery.

- Celery: good if you are familiar with it and already using it
- Huey: easier to setup than Celery but limited

## Run the worker

[Run the Centrifugo server](http://django-instant.readthedocs.io/en/latest/src/usage.html)

Run Redis and launch a Celery beat and a worker or a just a Huey worker:

  ```bash
celery -A project_name beat  -l info --broker='redis://localhost:6379/0'
celery -A project_name worker  -l info --broker='redis://localhost:6379/0'

# or
python manage.py run_huey
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

You can tweak ``presence/js/handlers.js`` to make your own client-side event handlers.

## How it works

The presence data is automaticaly updated from the time based worker asking Centrifugo who is on the socket. 
This data is broadcasted to the clients via the websocket.

Huey is limited to 1 minute but you can set this default update time to a lower value in the settings 
if you use Celery.

