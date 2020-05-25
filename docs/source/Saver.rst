Cortex Saver Reference
======================================

The saver is available as ``cortex.saver``.


Saver subscribes to all the relevant topics it is capable of consuming and saving to them to the database. 


1. API:

.. code-block::

  >>> from cortex.saver import Saver     
  >>> saver = Saver(database_url)     
  >>> data = 
  …     
  >>> saver.save('pose', data)
  
Which connects to a database, accepts data, as consumed from the message queue, and saves it to the database. 


2. CLI:

.. code-block::

  $ python -m cortex.saver save                   \
  -d/--database 'postgresql://127.0.0.1:5432'     \
  'pose'                                          \
  'pose.result'

Which accepts a topic name and a path to some raw data, as consumed from
the message queue, and saves it to a database. This way of invocation
runs the saver exactly once.

.. code-block::

  $ python -m cortex.saver run-saver              \
  'postgresql://127.0.0.1:5432'                   \
  'rabbitmq://127.0.0.1:5672/'
  
  
Which runs the saver as a service, which works with a message queue
indefinitely; the saver subscribes to all the relevant topics it is
capable of consuming and saving them to the database.


Functions:

.. function:: Saver.save(data)

    Which connects to a database, accepts data, as consumed from the message queue, and saves it to the database.