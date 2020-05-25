Cortex Parses Reference
======================================

The parsers are available at ``cortex.parsers``. 

Parsers are simple functions or classes, built on top of a platform (using aspect-oriented programming), and easily deployable as microservices consuming raw data
from the queue, and producing parsed results to it. 


INFO: Parsers can be added easily as decribed in `Adding Parsers <https://github.com/AvivYaniv/Cortex#adding-Parsers>`__ 


1. API:

.. code-block::

  >>> from cortex.parsers import run_parser     
  >>> data = …      
  >>> result = run_parser('pose', data)
  
Which accepts a parser name and some raw data, as consumed from the
message queue, and returns the result, as published to the message
queue. 

2. CLI:

.. code-block::

  $ python -m cortex.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
Which accepts a parser name and a path to some raw data, as consumed
from the message queue, and prints the result, as published to the
message queue (optionally redirecting it to a file). This way of
invocation runs the parser exactly once.

.. code-block::

  $ python -m cortex.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'

Which runs the parser as a service, which works with a message queue
indefinitely. The following parsers are available: 

1. Pose  

 Collects the translation and the rotation of the user's head at a given timestamp,
and publishes the result to a dedicated topic. 

2. Color Image  

 Collects the color image of what the user was seeing at a given timestamp, and
publishes the result to a dedicated topic. 


NOTE: the data itself is
stored to disk, and only the metadata published. 

3. Depth Image

 Collects the depth image of what the user was seeing at a given
timestamp, and publishes the result to a dedicated topic.  A depth image
is a width × height array of floats, where each float represents how far
the nearest surface from the user was, in meters. So, if the user was
looking at a chair, the depth of its outline would be its proximity to
her (for example, 0.5 for half a meter), and the wall behind it would be
farther (for example, 1.0 for one meter). 


NOTE: the data itself should
be stored to disk, and only the metadata published. 

4. Feelings
 Collects the feelings the user was experiencing at any timestamp, and
publishes the result to a dedicated topic.

Functions:

.. function:: run_parser(<parser_type>, data)

    Which accepts a parser name and a path to some raw data, as consumed from the message queue, and prints the result, as published to the message queue (optionally redirecting it to a file). This way of invocation runs the parser exactly once.
