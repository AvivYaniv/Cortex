Cortex Client Reference
======================================

The client is available as ``cortex.client``. 

Client used to upload an
``mind`` file to server, which is a presentation of telemetry snapshots.


1. API:

.. code-block::

  >>> from cortex.client import upload_sample     
  >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')     
  … # upload path to host:port``


2. CLI:

.. code-block::

  $ python -m cortex.client upload-sample    \
  -h/--host '127.0.0.1'                      \
  -p/--port 8000                             \
  'snapshot.mind.gz'     
  …``


Issues & Actions: 

1. File not found : client will write error message to
user, and then exit graciously.

2. Communication error : client will
exit graciously. 

3. Server is unavailable : client will retray to
connect for few times, and then exit if failed to connect.


Functions:

.. function:: upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')

    Uploads an `mind` file to the specified server.
Client Service: 

.. autoclass:: cortex.client.client_service.ClientService


