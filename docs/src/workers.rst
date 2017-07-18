Workers
=======

The presence data is automaticaly updated from the time based worker asking Centrifugo who is on the socket. 
This data is broadcasted to the clients over the websocket.

Default worker
--------------

The default worker for presence updates is a go module. Install with the 
command ``python manage.py installpres``: it will generate two files in your main project directory:

- ``centpres``: the executable
- ``centpres_config.json``: the config file

To run the worker: ``./centpres``. This will start updating presence info.

Note: you can also compile the go module from the source in *presence/go/src/*
