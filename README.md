# Django Presence

A widget that auto-updates the list of users present on the site.

This involves the following dependencies: 

- [Centrifugo](https://github.com/centrifugal/centrifugo/) for the websocket server.
- [Redis](http://redis.io/) for the data broker.
- [Celery](https://github.com/celery/celery) or [Huey](https://github.com/coleifer/huey) for the non blocking time based worker.
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
"presence",
# for huey add "huey.contrib.djhuey",
  ```

In settings.py:
  ```python
# this one is used for convenience so you don't have to include the app in the templates by yourself
INSTANT_APPS = ['presence']

# for celery:
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'update-presence': {
        'task': 'presence.tasks.update_presence',
        'schedule': timedelta(minutes=1),
    },
}

# for huey
from huey import RedisHuey
HUEY = RedisHuey('your_project_name')
  ```
  
Default async backend is Celery. You will need a ``celery.py`` file as explained [here](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html).

To use Huey add a ``ASYNC_BACKEND = "huey"`` in settings.

Run Redis and [launch the Centrifugo server](http://django-instant.readthedocs.io/en/latest/src/usage.html). 
Then launch a Celery beat and a worker or a just a Huey worker:

  ```bash
celery -A project_name beat  -l info --broker='redis://localhost:6379/0'
celery -A project_name worker  -l info --broker='redis://localhost:6379/0'

# or
python manage.py run_huey
  ``` 

Where you want the presence widget to be place `{% include "presence/widget.html" %}`.

You can tweak ``presence/js/handlers.js`` to add your own client-side event handlers.  

## How it works

The presence data is automaticaly updated every minute from the time based worker asking Centrifugo who is on the socket. 
This data is broadcasted to the clients via the websocket and as well stored into Redis.

The presence data for the initial client http connection (when the page loads) is retrieved from Redis, 
and later on the live updates will be performed via the websocket channel. 

In this design the server only pushes presence information every minute. There are no requests made from actions on the
client side: for example it could be possible to fetch fresh info on each client connection, but it could lead to some
unecessary ressources consumption, overloading scenarios or scaling problems. 

This app wants to be fast and reliable so giving the garantee to get an info of max age 1 minute looked 
sufficient here in order to preserve the performance and the stability.

