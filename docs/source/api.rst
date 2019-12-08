Brain Computer Interface API Reference
======================================

This is Brain Computer Interface's API reference.


.. function:: run_server(address, data_dir)

    Starts a server to which thoughts can be uploaded to with the `upload_thought` function.

.. function:: run_webserver(address, data_dir)

    Starts a server to which shows users thoughts

.. function:: upload_thought(address, user_id, thought)

     Sends to the server user's thought.
