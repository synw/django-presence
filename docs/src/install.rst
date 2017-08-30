Install
=======

Dependencies:

- `Centrifugo <https://github.com/centrifugal/centrifugo/>`_ : the websockets server
- `Django Instant <https://github.com/synw/django-instant>`_ : the Centrifugo <-> Django layer

Install Django Instant according to `this documentation <http://django-instant.readthedocs.io/en/latest/src/install.html>`_

``pip install django-presence``

Add ``"presence",`` to installed apps

Settings
--------

Centrifugo config: be sure to have presence enabled in ``config.json`` (cf django-instant docs):

.. highlight:: javascript

::
   
   {
    "secret": "70b651f6-775a-4949-982b-b387b31c1d84",
    "anonymous": true,
    "presence":true
    }
    
Settings:

.. highlight:: python

::
   
   # required
   SITE_SLUG = "mysite"
   # frequency of updates: optional: default is 10
   PRESENCE_FREQUENCY = 30
   
Templates
---------

Add a instant/extra_clients.js template with this content:

.. highlight:: django

::
   
   {% include "presence/js/client.js" %}

Add a instant/extra_handlers.js template with this content:

.. highlight:: django

::
   
   {% include "presence/js/handlers.js" %}

Where you want the presence widget to be put:

.. highlight:: django

::
   
   {% include "presence/widget.html" %}.

You can tweak ``presence/js/handlers.js`` to make your own client-side event handlers.
   