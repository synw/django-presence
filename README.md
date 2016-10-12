# Django Presence

A real time list of users on the site widget. This package provides a javascript client
that listens to a websocket channel, and a time based worker that updates the presence information.

Dependencies:

- [Centrifugo](https://github.com/centrifugal/centrifugo): the websockets server
- [Django Instant](https://github.com/synw/django-instant): the Django <-> Centrifugo layer

For install and usage read the [documentation](http://django-presence.readthedocs.io/en/latest/)