Cortex CLI Reference
======================================

The CLI is available as ``cortex.cli``. 

The CLI questions the API server
and reflects the results.

The CLI supports the following commands: 

1.

.. code:: sh

    $ python -m cortex.cli get-users

Returns the list of all the supported users, including their IDs and
names only.

2.

.. code:: sh

    $ python -m cortex.cli get-user <user-id>

Returns the specified user's details: ID, name, birthday and gender.

3.

.. code:: sh

    $ python -m cortex.cli get-snapshots <user-id>

Returns the list of the specified user's snapshot IDs and datetimes only.

4.

.. code:: sh

    $ python -m cortex.cli get-snapshot <user-id> <snapshot-id>

Returns the specified snapshot's details: ID, datetime, and the
available results' names only (e.g. pose).


5.

.. code:: sh

    $ python -m cortex.cli get-result <user-id> <snapshot-id> <result-name>

 Returns the specified snapshot's result. Supports: [pose, color-image,
depth-image, feelings]. 


All commands should accept the -h/--host and
-p/--port flags to configure the host and port, but default to the API's
address. The get-result command should also accept the -s/--save flag
that, if specified, receives a path, and saves the result's data to that
path.
