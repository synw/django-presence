# django-presence

User presence monitoring app for Django. A widget that auto-updates the list of users present on the site.

This involves the following dependencies: 

[Centrifugo](https://github.com/centrifugal/centrifugo/) for the websocket server.
[Redis](http://redis.io/) for the data broker.
[Huey](https://github.com/coleifer/huey) for the time based workers.
[Django Instant](https://github.com/synw/django-instant) for the Centrifugo/Django layer.
