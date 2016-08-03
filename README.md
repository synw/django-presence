# Django Presence

A widget that auto-updates the list of users present on the site.

This involves the following dependencies: 

- [Centrifugo](https://github.com/centrifugal/centrifugo/) for the websocket server.
- [Redis](http://redis.io/) for the data broker.
- [Huey](https://github.com/coleifer/huey) for the non blocking time based worker.
- [Django Instant](https://github.com/synw/django-instant) for the Centrifugo/Django layer.

## Install

First set up Centrifugo and Django Instant:
 [instructions here](http://django-instant.readthedocs.io/en/latest/src/install.html)
 
Then Redis and Huey:

  ```bash
sudo aptitude install redis-server # example for debian
pip install redis huey
  ```

## Configure and run

Configure Centrifugo to handle presence info: in config.json:

  ```javascript
{
	"secret": "70b651f6-775a-4949-982b-b387b31c1d84",
	"anonymous": true,
	"presence":true
}
  ```

In INSTALLED_APPS:

  ```python
"huey.contrib.djhuey",
"presence",
  ```

In settings.py:
  ```python
RedisHuey('your_project_name')
from huey import RedisHuey
  ```

Run Redis and [launch the Centrifugo server](http://django-instant.readthedocs.io/en/latest/src/usage.html). 
Then launch a Huey worker:

  ```bash
python manage.py run_huey
  ```

Last step: the templates: 

Where you want the presence widget to be place `{% include "presence/widget.html" %}`.

Now copy the template `instant/templates/instant/js/handlers.js` to `templates/instant/js/handlers.js` and add 
the presence app in it like this:

  ```django
function handlers_for_event_class(event_class, channel, message) {
	// just add this line:
	{% include "presence/js/handlers.js" %}
	// other events
	if (event_class == 'Important') {
		// ...
		return true
	}
	return true
}
  ```
You can tweak ``presence/js/handlers.js`` to add your own client-side event handlers.  

## How it works

The presence data is automaticaly updated every minute from the Huey worker asking Centrifugo who is on the socket. 
This data is broadcasted to the clients via the websocket and as well stored into Redis.

The presence data for the initial client http connection (when the page loads) is retrieved from Redis, 
and later on the live updates will be performed via the websocket channel. 

In this design the server only pushes presence information every minute. There are no requests made from actions on the
client side: for example it could be possible to fetch fresh info on each client connection, but it could lead to some
kind of overloading scenarios, scaling problems and unecessary ressources consumption. 

This app wants to be fast and reliable so giving the garantee to get an info of max age 1 minute looked 
sufficient here in order to preserve the performance and the stability.

