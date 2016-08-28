# Django Presence

A widget that auto-updates the list of users present on the site.

This involves the following dependencies: 

- [Centrifugo](https://github.com/centrifugal/centrifugo/) for the websocket server.
- [Django Instant](https://github.com/synw/django-instant) for the Centrifugo/Django layer.

## Install

First set up Centrifugo and Django Instant:
 [instructions here](http://django-instant.readthedocs.io/en/latest/src/install.html)
 
Then Redis and Huey or Celery:

  ```bash
sudo apt-get install redis-server # example for debian
pip install redis celery
# or pip install redis huey
  ```

## Configure and run

Configure Centrifugo to handle presence info: in ``config.json``:

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
# for huey add "huey.contrib.djhuey",
  ```

In settings.py:
  ```python

# for celery:
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'update-presence': {
        'task': 'presence.tasks.update_presence',
        'schedule': timedelta(minutes=1),
    },
}

# for huey
PRESENCE_ASYNC_BACKEND = "huey"
from huey import RedisHuey
HUEY = RedisHuey('your_project_name')
  ```
  
Default async backend is Celery. You will need a ``celery.py`` file as explained 
[here](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)

Run Redis and [launch the Centrifugo server](http://django-instant.readthedocs.io/en/latest/src/usage.html). 
Then launch a Celery beat and a worker or a just a Huey worker:

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

You can tweak ``presence/js/handlers.js`` to add your own client-side event handlers.

## How it works

The presence data is automaticaly updated every minute from the time based worker asking Centrifugo who is on the socket. 
This data is broadcasted to the clients via the websocket.

In this design the server only pushes presence information every minute. There are no requests made from actions on the
client side: for example it could be possible to fetch fresh info on each client connection, but it could lead to some
unecessary ressources consumption, overloading scenarios or scaling problems. 

This app wants to be fast and reliable so giving the garantee to get an info of max age 1 minute looked 
sufficient here in order to preserve the performance and the stability. You can set this default update time
to a lower value in seconds in the Celery settings. Huey is limited to 1 minute.

