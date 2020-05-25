Cortex API Server Reference
======================================

The API is available as ``cortex.api``.

The API server questions the database and reflects the results. 



INFO!
The API server results are in
`JSON <https://en.wikipedia.org/wiki/JSON>`__ format, but the format can
be customized easily as described in `API
Format <https://github.com/AvivYaniv/Cortex/blob/master/README.md#551-api-format>`__.



The API server utilities
`Flask-RESTful <https://flask-restful.readthedocs.io/en/latest/>`__.




INFO! The API URLs format mentioned in API service easily support any
other web-framework URLs format as described in `API
URLs <https://github.com/AvivYaniv/Cortex/blob/master/README.md#552-api-urls>`_.



1. API:

.. code-block::

  >>> from cortex.api import run_api_server
  >>> run_api_server(
  ...     host 		= '127.0.0.1',
  ...     port 		= 5000,
  ...     database_url	= 'postgresql://127.0.0.1:5432',
  ... )
  … # listen on host:port and serve data from database_url

2. CLI:

.. code-block::

  $ python -m cortex.api run-server             \
  	-h/--host '127.0.0.1'                   \
  	-p/--port 5000                          \
  	-d/--database 'postgresql://127.0.0.1:5432'

The API server supports the following RESTful API endpoints: 

.. csv-table:: 
   :header: "No.", "URL", "Description"
   :widths: 30, 300, 900

   "1", "GET /users", "Returns the list of all the supported users, including their IDs and names only."
   "2", "GET /users/user-id", "Returns the specified user's details: ID, name, birthday and gender."
   "3", "GET /users/user-id/snapshots", "Returns the list of the specified user's snapshot IDs and datetimes"
   "4", "GET /users/user-id/snapshots/snapshot-id", "Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose)."
   "5", "GET /users/user-id/snapshots/snapshot-id/result-name", "Returns the specified snapshot's result. Supports: [pose, color-image, depth-image, feelings], where anything that has large binary data should contain metadata only, with its data being available via some dedicated URL (that is mentioned in its metadata), like so: GET /users/user-id/snapshots/snapshot-id/color-image/data"



Functions:

.. function:: run_api_server(host, port, database_url)

    Starts an API server that replays to the URL queries mentioned above.

