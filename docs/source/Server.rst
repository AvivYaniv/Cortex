Cortex Server Reference
======================================

The server is available as ``cortex.server``. 

The server accepts clients
connection, receive the uploaded ``mind`` file and publish them to its
message queue. 

1. API:

::

  
  >>> from cortex.server import run_server     
  >>> def print_message(message):     
  ...     print(message)     
  >>> run_server(host='127.0.0.1', port=8000, publish=print_message)     
  … # listen on host:port and pass received messages to publish``


2. CLI:

::

  $ python -m cortex.server run-server    \
  -h/--host '127.0.0.1'                   \
  -p/--port 8000                          \
  'rabbitmq://127.0.0.1:5672/'
  
  
Issues & Actions: 

1. Multiple clients upload at the same time: the
server will handle all clients requests. 

2. Communication error: The
server client's handler will stop graciously, no other clients (present
or future) are effected. 

3. Server accepts snapshots that already have
been accepted: server would detect the duplicate upload, and not publish
any of the snapshots that have already been handled.



API Functions:

.. function:: run_server(host='127.0.0.1', port=8000, publish=print_message)

    Listen on host:port and pass received messages to publish.

Server Service: 

.. autoclass:: cortex.server.server_service.ServerService

