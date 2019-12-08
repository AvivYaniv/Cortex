Brain Computer Interface CLI Reference
======================================

The `Cortex` package provides a command-line interface:

.. code:: bash

    $ python -m Cortex
    ...

The top-level options include:

- ``-q``, ``--quiet``

    This option suppresses the output.

- ``-t``, ``--traceback``

    This option shows the full traceback when an exception is raised (by
    default, only the error message is printed, and the program exits with a
    non-zero code).

To see its version, run:

.. code:: bash

    $ python -m Cortex --version
    Cortex, version 0.1.0
    ...
    
The CLI provides the `run-server` command:
	This command starts a server to which thoughts can be uploaded to with the `upload_thought` command
	<br/>Usage: run-server [address] [data_dir]

.. code:: bash

	    $ python -m Cortex run-server '127.0.0.1:8000' 'data'
    ...

The CLI further provides the `run-webserver` command:
	This command starts a server to which shows users thoughts
	<br/>Usage: run-webserver [address] [data_dir]

.. code:: bash

    $ python -m Cortex run-webserver '127.0.0.1:8000' 'data'
    ...

The CLI further provides the `upload-thought` command:
	This command sends to the server user's thought
	<br/>Usage: upload-thought [address] [user_id] [thought]

.. code:: bash

    $ python -m Cortex run-webserver '127.0.0.1:8000' 123 'sabich'
    ...
