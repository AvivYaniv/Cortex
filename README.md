![build status](https://api.travis-ci.com/AvivYaniv/Cortex.svg?branch=master)
![coverage](https://codecov.io/gh/AvivYaniv/Cortex/branch/master/graph/badge.svg)
![docs](https://readthedocs.org/projects/braincomputerinterface/badge/?version=latest)

# Cortex

Cortex is an *ultra **flexibale** and **durable*** brain-comuter-interface project, which enabels to upload and view users telemetry data. 
<br/>See [full documentation](https://braincomputerinterface.readthedocs.io/en/latest/).

Telemetry data currently contains snapshots of:
1. User feelings: consists of the following [hunger, thirst, exhaustion, happiness], and ranged between [-1,1].
2. [Pose](https://en.wikipedia.org/wiki/Pose_(computer_vision)): a computer-vision concept to determine object's position (user) and orientation relative to some coordinate system, and consists of two vectors: [ Translation, Rotation ].
3. Color image: shows what the user sees.
4. Depth image: shows 'heatmap' of how far the nearest surface from the user was.

Cortex project is the final project of [Advanced System Design](https://advanced-system-design.com/) at Tel-Aviv Univeristy by [Dan Gittik](https://dan-gittik.com/).

<p align="center">
    <img src="https://github.com/AvivYaniv/Cortex/blob/master/about/Demo/CortexDemo.gif?raw=true"/>
<p/>

## Table Of Contents

1. [Architecture](https://github.com/AvivYaniv/Cortex/blob/master/README.md#architecture) <br/>
2. [Installation](https://github.com/AvivYaniv/Cortex/blob/master/README.md#installation) <br/>
3. [Modules](https://github.com/AvivYaniv/Cortex/blob/master/README.md#3-modules) <br/>
3.1. [Client](https://github.com/AvivYaniv/Cortex/blob/master/README.md#31-client) <br/>
3.2. [Server](https://github.com/AvivYaniv/Cortex/blob/master/README.md#32-server) <br/>
3.3. [Parsers](https://github.com/AvivYaniv/Cortex/blob/master/README.md#33-parsers) <br/>
3.4. [Savers](https://github.com/AvivYaniv/Cortex/blob/master/README.md#34-savers) <br/>
3.5. [API](https://github.com/AvivYaniv/Cortex/blob/master/README.md#35-api) <br/>
3.6. [GUI](https://github.com/AvivYaniv/Cortex/blob/master/README.md#36-gui) <br/>
3.7. [CLI](https://github.com/AvivYaniv/Cortex/blob/master/README.md#37-cli) <br/>
4. [Frameworks](https://github.com/AvivYaniv/Cortex/blob/master/README.md#4-frameworks) <br/>
4.1. [MessageQueue](https://github.com/AvivYaniv/Cortex/blob/master/README.md#41-messagequeue) <br/>
4.2. [DataBase](https://github.com/AvivYaniv/Cortex/blob/master/README.md#42-database) <br/>
4.3. [Log](https://github.com/AvivYaniv/Cortex/blob/master/README.md#43-log) <br/>
5. [Flexability and SOLIDness](https://github.com/AvivYaniv/Cortex/blob/master/README.md#5-flexability-and-solidness) <br/>
5.1. Client <br/>
5.1.1. File Readers and Writers <br/>
5.1.2. Mind File Formats <br/>
5.1.3. Client-Server Protocol <br/>
5.2. Parsers <br/>
5.3. MessageQueue <br/>
5.3.1. MessageQueue Context Configuration <br/>
5.3.2. MessageQueue Driver <br/>
5.3.3. MessageQueue Messages <br/>
5.4. DataBase <br/>
5.4.1. DataBase Driver <br/>
5.5. API <br/>
5.5.1. API Format <br/>
5.5.2. API URLs <br/>
5.6. GUI <br/>
5.6.1. Bar Charts <br/>
5.6.2. Multiline Graphs <br/>
6. Tests <br/>
6.1. Test tools <br/>
7. [Additional Information](https://github.com/AvivYaniv/Cortex/blob/master/README.md#7-additional-information) <br/>
7.1. [Scripts](https://github.com/AvivYaniv/Cortex/blob/master/README.md#71-scripts) <br/>
7.2. [Docker](https://github.com/AvivYaniv/Cortex/blob/master/README.md#72-docker) <br/>
7.2.1. [Docker startup](https://github.com/AvivYaniv/Cortex/blob/master/README.md#721-docker-startup) <br/>
7.2.2. [How to add new micro-service](https://github.com/AvivYaniv/Cortex/blob/master/README.md#722-how-to-add-new-micro-service) <br/>

## Architecture

The Cortex project contains of client that communicates to server user's telemetry data, as matter of [lifelogging](https://en.wikipedia.org/wiki/Lifelog).

The server passes the snapshot messages to a message-queue. <br/>
Parser micro-services consume from the message-queue the raw snapshots and push to the message-queue the parsed results. <br/>
Savers pull from the message-queue the parsed results, in a load-balanced manner, and save them to the database.

Project also provides a GUI server to which users can connect to view telemetry data.

Other micro-services that are included are API to pull data from the database and CLI which reflects the API.

![alt text](https://github.com/AvivYaniv/Cortex/blob/master/about/Architecture/Architecture.png?raw=true)

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:AvivYaniv/Cortex.git
    ...
    $ cd Cortex/
    ```

2. Run the presequites script to install project presequites (i.e. docker, docker-compose):

    ```sh
    $ ./scripts/presequites.sh    
    ```

3. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [Cortex] $ # you're good to go!
    ```

4. Lastly, run the `run-pipeline.sh` script to create docker containers:

   ```sh
   [Cortex] $ ./scripts/run-pipeline.sh
   ```

NOTE! Creation of docker containers may take some time <br/>
NOTE! During that proccess, micro-services that use the database and message-queue would try to connect to them, until they are available, errors seen during that period can be ignored.<br/>

5. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## 3. Modules
### 3.1. Client
The client is available as `cortex.client`. <br/>
Client used to upload a `mind` file to server, which is a presentation of telemetry snapshots. <br/>
1. API:
    ```python
    >>> from cortex.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to host:port
    ```
2. CLI:
    ```sh
    $ python -m cortex.client upload-sample    \
      -h/--host '127.0.0.1'                    \
      -p/--port 8000                           \
      'snapshot.mind.gz'
	…
    ```
<br/>
Issues & Actions:<br/>
1. File not found : client will write error message to user, and then exit graciously. <br/>
2. Communication error : client will exit graciously. <br/>
3. Server is unavailable : client will retray to connect for few times, and then exit if failed to connect. <br/>
<br/>

### 3.2. Server
The server is available as `cortex.server`. <br/>
The server accepts clients connection, receive the uploaded `mind` file and publish them to its message queue. <br/>
1. API:
    ```python
	>>> from cortex.server import run_server
	>>> def print_message(message):
	...     print(message)
	>>> run_server(host='127.0.0.1', port=8000, publish=print_message)
	… # listen on host:port and pass received messages to publish
    ```
2. CLI:
    ```sh
	python -m cortex.server run-server    \
	 -h/--host '127.0.0.1'                \
	 -p/--port 8000                       \
	 'rabbitmq://127.0.0.1:5672/'
    ```
<br/>
Issues & Actions:<br/>
1. Multiple clients uploat at the same time : server will handle all clients requests. <br/>
2. Communication error : server client's handler will stop graciously, no other clients (present or future) are effected. <br/>
3. Server accepts snapshhots that already have been accepted : server would detect the duplicate upload, and not publish any of the snapshots that have already been handled. <br/>
<br/>

### 3.3. Parsers
The parsers are available at `cortex.parsers`. <br/>
Parsers are simple functions or classes, built on top of a platform (using aspect-oriented programming), and easily deployable as microservices consuming raw data from the queue, and producing parsed results to it. <br/>
INFO: Parsers can be added easily as decribed in [Adding Parsers](https://github.com/AvivYaniv/Cortex#adding-Parsers) <br/>
1. API:
    ```python
    >>> from cortex.parsers import run_parser
    >>> data = … 
    >>> result = run_parser('pose', data)
    ```
    Which accepts a parser name and some raw data, as consumed from the message queue, and returns the result, as published to the message queue.
2. CLI:
    ```sh
    $ python -m cortex.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
    ```
    Which accepts a parser name and a path to some raw data, as consumed from the message queue, and prints the result, as published to the message queue (optionally redirecting it to a file). This way of invocation runs the parser exactly once. <br/>
    ```sh
    $ python -m cortex.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
    ```
    Which runs the parser as a service, which works with a message queue indefinitely. <br/>
<br/>
The following parsers are available: <br/>
1. Pose <br/>
&emsp;Collects the translation and the rotation of the user's head at a given timestamp, and publishes the result to a dedicated topic. <br/>
2. Color Image <br/>
&emsp;Collects the color image of what the user was seeing at a given timestamp, and publishes the result to a dedicated topic. <br/>
NOTE: the data itself is stored to disk, and only the metadata published. <br/>
3. Depth Image <br/>
&emsp;Collects the depth image of what the user was seeing at a given timestamp, and publishes the result to a dedicated topic.<br/>
&emsp;A depth image is a width × height array of floats, where each float represents how far the nearest surface from the user was, in meters. So, if the user was looking at a chair, the depth of its outline would be its proximity to her (for example, 0.5 for half a meter), and the wall behind it would be farther (for example, 1.0 for one meter).
NOTE: the data itself should be stored to disk, and only the metadata published.<br/>
4. Feelings <br/>
&emsp;Collects the feelings the user was experiencing at any timestamp, and publishes the result to a dedicated topic. <br/>
<br/>

### 3.4. Savers
The saver is available as `cortex.saver`. <br/>
Saver subscribes to all the relevant topics it is capable of consuming and saving to them to the database. <br/>
1. API:
    ```python
    >>> from cortex.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)
    ```
    Which connects to a database, accepts a topic name and some data, as consumed from the message queue, and saves it to the database.
2. CLI:
    ```sh
    $ python -m cortex.saver save                   \
     -d/--database 'postgresql://127.0.0.1:5432'    \
     'pose'                                         \
     'pose.result' 
    ```
    Which accepts a topic name and a path to some raw data, as consumed from the message queue, and saves it to a database. This way of invocation runs the saver exactly once. <br/>
    ```sh
    $ python -m cortex.saver run-saver              \
      'postgresql://127.0.0.1:5432'                 \
      'rabbitmq://127.0.0.1:5672/' 
    ```
    Which runs the saver as a service, which works with a message queue indefinitely; the saver subscribes to all the relevant topics it is capable of consuming and saving them to the database. <br/>
<br/>

### 3.5. API
The API is available as `cortex.api`. <br/>

The API server questions the database and reflects the results. <br/>
INFO! The API server results are in [JSON](https://en.wikipedia.org/wiki/JSON) format, but format can be costumized easily as described in [API Format](https://github.com/AvivYaniv/Cortex/blob/master/README.md#551-api-format) in this document. <br/>

The API server utilities [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/). <br/>
INFO! The API URLs format mentioned in API service easily support any other web-framework as described in [API URLs](https://github.com/AvivYaniv/Cortex/blob/master/README.md#552-api-urls) in this document. <br/>
1. API:
    ```python
    >>> from cortex.api import run_api_server
    >>> run_api_server(
    ...     host 		= '127.0.0.1',
    ...     port 		= 5000,
    ...     database_url 	= 'postgresql://127.0.0.1:5432',
    ... )
    … # listen on host:port and serve data from database_url
    ```
2. CLI:
    ```sh
    $ python -m cortex.api run-server    \
     -h/--host '127.0.0.1'               \
     -p/--port 5000                      \
     -d/--database 'postgresql://127.0.0.1:5432'
    ```
<br/>
The API server supports the following RESTful API endpoints: <br/>
1. GET /users <br/>
&emsp;Returns the list of all the supported users, including their IDs and names only. <br/>
2. GET /users/user-id <br/>
&emsp;Returns the specified user's details: ID, name, birthday and gender. <br/>
3. GET /users/user-id/snapshots <br/>
&emsp;Returns the list of the specified user's snapshot IDs and datetimes only. <br/>
4. GET /users/user-id/snapshots/snapshot-id <br/>
&emsp;Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose). <br/>
5. GET /users/user-id/snapshots/snapshot-id/result-name <br/>
&emsp;Returns the specified snapshot's result. Supports: [pose, color-image, depth-image, feelings], where anything that has large binary data should contain metadata only, with its data being available via some dedicated URL (that is mentioned in its metadata), like so: GET /users/user-id/snapshots/snapshot-id/color-image/data <br/>
<br/>

### 3.6. GUI
The GUI server is available as `cortex.gui`. <br/>
The GUI consumes data from the API server and reflect it in a beautiful and user-friendly mannner. <br/>
Pages:<br/>
1. HomePage: allows to select user based on either [ user-name, user-id ].  <br/>
2. User Snapshots : displays selected users snapshots in an interactive manner.  <br/>
Features: <br/>
1. Dark Mode. <br/>
2. Dynamic and interactive snapshots : you can move between snapshots just by moving the mouse. <br/>
:egg: Easter Egg : Follow the breadcrumbs hints, start from hovering the logo. <br/>
 <br/>
 
1. API:
    ```python
    >>> from cortex.gui import run_server
    >>> run_server(
    ...     host        = '127.0.0.1',
    ...     port        = 8080,
    ...     api_host    = '127.0.0.1',
    ...     api_port    = 5000,
    ... )
    ```
    Which runs the GUI server, which consumes data from the API server. <br/>
2. CLI:
    ```sh
    $ python -m cortex.gui run-server          \
     -h/--host '127.0.0.1'                     \
     -p/--port 8080                            \
     -H/--api-host '127.0.0.1'                 \
     -P/--api-port 5000
    ```
    Which runs the GUI server, which consumes data from the API server. <br/>
<br/>

### 3.7. CLI
The CLI is available as `cortex.cli`. <br/>
The CLI questions the API server and reflects the results. <br/>
<br/>
The CLI supports the following commands: <br/>
<br/>
1. 
```sh
$ python -m cortex.cli get-users
```
<br/>&emsp;Returns the list of all the supported users, including their IDs and names only. <br/>
2. 
```sh
$ python -m cortex.cli get-user <user-id>
```
<br/>&emsp;Returns the specified user's details: ID, name, birthday and gender. <br/>
3. 
```sh
$ python -m cortex.cli get-snapshots <user-id>
```
<br/>&emsp;Returns the list of the specified user's snapshot IDs and datetimes only. <br/>
4. 
```sh
$ python -m cortex.cli get-snapshot <user-id> <snapshot-id>
```
<br/>&emsp;Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose). <br/>
5. 
```sh
$ python -m cortex.cli get-result <user-id> <snapshot-id> <result-name>
```
<br/>&emsp;Returns the specified snapshot's result. Supports: [pose, color-image, depth-image, feelings].
<br/>
All commands should accept the -h/--host and -p/--port flags to configure the host and port, but default to the API's address. <br/>
The get-result command should also accept the -s/--save flag that, if specified, receives a path, and saves the result's data to that path. <br/>
<br/>

## 4. Frameworks
The Cortex project uses the following advanced yet simple-to-use frameworks:
<br/>
### 4.1. MessageQueue
The Cortex project uses the [RabbitMQ](https://www.rabbitmq.com/) message-broker which implements the [Advanced Message Queuing Protocol (AMQP)](https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol). <br/>
As stated above, generic framework that decouples the project from the selected message-queue technology, has been developed to support **ANY** publisher-consumer implementation in an easy way. <br/>

The MessageQueue Framework, composed of transmitters (i.e. Publisher) and receivers (i.e. Consumer) and is configuration-based. <br/>

NOTE! The terms [ transmitter, receiver ] and [ publisher, consumer ] will be used interchangeably, yet the former are concrete instances for the [ publisher, consumer ] concept. <br/>

The following UML diagram depicts the replationships between the main components: <br/>
<p align="center">
    <img src="https://github.com/AvivYaniv/Cortex/blob/master/about/Design/MessageQueueDesign.png?raw=true"/>
<p/>
<br/>

MessageQueue Framework components: <br/>
1. MessageQueue Context: <br/>
The framework relies on the understanding that diffrent publisher-consumer implementations would require diffrent parameters for initialization and running configuration. <br/>

The `MessageQueueContext` is an object that holds all neccessary information to initialize and run an instance of either [ publisher, consumer ].

The `MessageQueueContext` is loaded based on a configuration-file that is written for a specific message-queue implementation (i.e. RabbitMQ).

The `MessageQueueContext` object mandatorily holds information regerding it's role [ transmitter, receiver ]. <br/>

EXAMPLE: An example of RabbitMQ [message-queue context configuration file](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/context/rabbitmq_config.yaml). <br/>

INFO! MessageQueue Context configuration supports *any* dictionary-based file (i.e. YAML) and enabels to *dynamically set values in run-time*, for more information please see [MessageQueue Context Configuration](https://github.com/AvivYaniv/Cortex/blob/master/README.md#531-messagequeue-context-configuration). <br/> 

INFO! MessageQueue Context should be created with the [`MessageQueueContextFactory`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/context/message_queue_context_factory.py), which loads the concrete MessageQueue Context configuration file based it's sole `message_queue_type` initialization parameter. <br/>

2. MessageQueue Abstract Base Class: <br/>
This class gets a message-queue context and runs as a transmitter (i.e. Publisher) or a receiver (i.e. Consumer). <br/>
Diffrent message-queue implementations do inherit from this abstract class which takes care for the common logic for initalization and calls the specifics for implementation running as either [ transmitter, receiver ]. <br/>

IMPORTANT! The [`MessageQueue`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/message_queue.py) is an abstract class and implementation should be provided to run specific message-queue technology (i.e. creating sub-class [`RabbitMQMessageQueue`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/rabbitmq_mq.py) for RabbitMQ). <br/>

INFO! You can change to any other message-queue technology, as described in [MessageQueue Driver](https://github.com/AvivYaniv/Cortex/blob/master/README.md#532-messagequeue-driver) in this document.

3. MessageQueue Publishers: <br/>
The MessageQueue Publisher can be run either: <br/>
<br/>

&emsp; 1. 
In a dedicated thread as [`MessageQueuePublisherThread`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/publisher/message_queue_publisher_thread.py) (to handle [IO Events Loop](https://en.wikipedia.org/wiki/Event_loop)). <br/>

&emsp; 2. 
In the same thread as [`MessageQueuePublisher`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/publisher/message_queue_publisher.py). <br/>
<br/>

IMPORTANT! The MessageQueue Publisher activates, yet decoupled from, the concrete technology implementation; which is dynamically loaded based on the `message_queue_type` parameter and initialized based on a `MessageQueueContext` which is passed with the `message_queue_context` parameter. <br/>

4. MessageQueue Consumers: <br/>
The MessageQueue Consumer can be run either: <br/>
<br/>

&emsp; 1. 
In a dedicated thread as [`MessageQueueConsumerThread`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/consumer/Message_queue_consumer_thread.py) (to handle [IO Events Loop](https://en.wikipedia.org/wiki/Event_loop), or if more than one consumer is required). <br/>

&emsp; 2. 
In the same thread as [`MessageQueueConsumer`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/consumer/message_queue_consumer.py). <br/>
<br/>

IMPORTANT! The MessageQueue Consumer activates, yet decoupled from, the concrete technology implementation; which is dynamically loaded based on the `message_queue_type` parameter and initialized based on a `MessageQueueContext` which is passed with the `message_queue_context` parameter. <br/>

5. MessageQueue Runner: <br/>
The MessageQueue Runner is the main component responsible of decoupling the MessageQueue Framework logic and implementation. <br/>
As such, it contains [ installing-message-queue, running-message-queue, stopping-message-queue ] methods which dynamically load the concrete implementation at runtime, based on the `message_queue_type` parameter. <br/>

### 4.2. DataBase

The Cortex project uses the [MongoDB](https://www.mongodb.com/) database which is a [NoSQL](https://en.wikipedia.org/wiki/NoSQL) database. <br/>
As stated above, generic framework that decouples the project from the selected database technology, has been developed to support **ANY** database implementation in an easy way. <br/>

The DataBase Framework is driver oriented. <br/>

The following UML diagram depicts the replationships between the main components: <br/>
<p align="center">
    <img src="https://github.com/AvivYaniv/Cortex/blob/master/about/Design/DataBaseDesign.png?raw=true"/>
<p/>
 <br/>

DataBase Framework components: <br/>
1. DataBase Abstact Base Class: <br/>
 This abstract class gets `database_type` and runs client that communicates with it. <br/>
Diffrent database implementations do inherit from this abstract class which takes care for the common logic for initalization and calls the specifics for implementation. <br/>

IMPORTANT! The [`_DataBaseBase`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/database/database_base.py) is an abstract class and implementation should be provided to run project database (i.e. creating sub-class [`_DataBaseCortex`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/database/database_cortex.py) for Cortex Project). <br/>

2. DataBase Driver: <br/>
 This abstract class gets `database_type` and runs client that communicates with it. <br/>
Diffrent database implementations do inherit from this abstract class which takes care for the common logic for initalization and calls the specifics for implementation. <br/>

IMPORTANT! The [`__DataBaseDriver`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/database/database_driver.py) is an abstract class and implementation should be provided to run specific database technology (i.e. creating sub-class [`MongoDBDataBase`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/database/mongodb_db.py) for MongoDB). <br/>

INFO! You can change to any other database technology, as described in [DataBase Driver](https://github.com/AvivYaniv/Cortex/blob/master/README.md#541-database-driver) in this document.

3. DataBase Runner: <br/>
The DataBase Runner is the main component responsible of decoupling the DataBase Framework logic and implementation. <br/>
As such, it contains [ installing-databse-queue, running-databse-queue, stopping-databse-queue ] methods which dynamically load the concrete implementation at runtime, based on the `database_type` parameter. <br/>

### 4.3. Log

The Cortex project uses the [ColorLog](https://github.com/borntyping/python-colorlog) logger. <br/>

INFO! The logger configuration can be read from any dictionary-based file (i.e. YAML), using the [`_LoggerLoader`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/logger/logger_loader.py). <br/>

## 5. Flexability and [SOLIDness](https://en.wikipedia.org/wiki/SOLID)

The Cortex project is built to be flexibale for modification and customizations.

> "Make the easy things easy, and the hard things possible" ~ Larry Wall (Programming Perl, 2nd Edition (1996), by Larry Wall, Tom Christiansen and Randal Schwartz)

### 5.1. Client

#### 5.1.1. File Readers and Writers
A driver oriented framework facilitates reading from and writing to diffrent files, based on their extension. <br/>
<br/>
File Readers Drivers: <br/>
To add new readers to [`FileReaderDriver`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/utils/files/file_reader_driver.py), simply add new entry to the `FILE_READER_DRIVERS ` dictionary, in which the key is the file extension and the value is the library for reading from file. <br/>
ASSUMPTION! It is confidently assumed that the library contains the following methods: `open(file_path, <mode>)` to open file, `read(size)` for reading, and `close()` for closing file. <br/>
<br/>
To add new writers to [`FileWriterDriver`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/utils/files/file_writer_driver.py), simply add new entry to the `FILE_WRITER_DRIVERS ` dictionary, in which the key is the file extension and the value is the library for reading from file. <br/>

ASSUMPTION! It is confidently assumed that the library contains the following methods: `open(file_path, <mode>)` to open file, `write(data)` for writing, and `close()` for closing file. <br/>

#### 5.1.2. Mind File Formats
A driver oriented framework facilitates reading from and writing to diffrent mind file formats, based on the `version` parameter. <br/>
<br/>
To add new format, take the following easy and simple steps: <br/>
1. Add new version name to [`ReaderVersions`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/readers/reader_versions.py). <br/>
2. Create new class that inherits from [`FileReaderBase`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/readers/file_reader.py), and implements the following methods: `read_user_information` and `read_snapshot`. <br/>


Reader class must contain a `version` field and this would be the name for reading files according to this reader.<br/>

Reader class must contain the following functions: <br/>
`__init__`			: That recives the file path to be read. <br/>
`read_user_information` 	: To read user information. <br/>
`read_snapshot` 		: To read snapshots. <br/>

<br/>

The file will be opened, user information will be read and then the snapshots.<br/>

To note a reader class, end it with `Reader` suffix.<br/>
<br/>i.e.
```python
class YourReader:

	version = 'your_format_name'

	def __init__(self, file_path):
		# Your code goes here

	def read_user_information(self):
		# Your code goes here

	def read_snapshot(self):
		# Your code goes here
```

EXAMPLE! Take a look at [`ProtobufMindReader`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/readers/mind/protobuf_mind_reader.py), and [`BinaryMindReader`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/readers/mind/binary_mind_reader.py). <br/>

3. Create new class that inherits from [`FileWriterBase`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/writers/file_writer.py), and implements the following methods: `write_user_information` and `write_snapshot`. <br/>


Writer class must contain a `version` field and this would be the name for writing files according to this writer. <br/>
<br/>
Writer class must contain the following functions: <br/>
`__init__`			: That recives the file path to be written. <br/>
`write_user_information` 	: To write user information. <br/>
`write_snapshot` 		: To write snapshots. <br/>
<br/>
The file will be opened, user information will be written and then the snapshots.

To note a writer class, end it with `Writer` suffix.
<br/>i.e.
```python
class YourWriter:

	version = 'your_format_name'

	def __init__(self, file_path):
		# Your code goes here

	def write_user_information(self):
		# Your code goes here

	def write_snapshot(self):
		# Your code goes here
```

EXAMPLE! Take a look at [`ProtobufMindWriter`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/writers/mind/protobuf_mind_writer.py), and [`BinaryMindWriter`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/writers/mind/binary_mind_writer.py). <br/>

#### 5.1.3. Client-Server Protocol
A generic framework facilitates client-server communication in easy and format-decoupled manner. <br/>

Current protocol format is [protobuf](https://developers.google.com/protocol-buffers)-based, and easily extensible and modifyable based on the [protocol.proto](https://github.com/AvivYaniv/Cortex/blob/master/cortex/protobuf/protos/protocol.proto) file definition. <br/>

Client-Server communication protocol format is being controlled in a *single* place, based on default `protocol_type` parameter resultion at [`Protocol`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/protocol/protocol.py). <br/>

NOTE! To change protocol implementation format, simply create a new folder in [Protocol](https://github.com/AvivYaniv/Cortex/tree/master/cortex/protocol) directory, named after the new protocol implementation format, and create in in classes for all the messages types that are in the [Protocol](https://github.com/AvivYaniv/Cortex/tree/master/cortex/protocol) directory. <br/>

EXAMPLE! Take a look at [Protobuf Protocol](https://github.com/AvivYaniv/Cortex/tree/master/cortex/protocol/protobuf), and the obsolete [Native Protocol](https://github.com/AvivYaniv/Cortex/tree/master/cortex/protocol/native). <br/>

<br/>

### 5.2. Parsers
You can add costume parsers, thus parsing data from the raw snapshots. <br/>
You can add new Parser with function or with dedicated class. <br/>
<br/>
To add new parser, by function (parser that dosen't require inner state), take the following easy and simple step:
<br/>
Create a new file containig parser function, in the [`Snapshots Parsers`](https://github.com/AvivYaniv/Cortex/tree/master/cortex/parsers/snapshot) directory. <br/>
To note a parser function, end it with `_parser` suffix.
<br/>
i.e.

```python
def your_parser(snapshot):
    # Your code goes here
your_parser.field = 'your_parser_field_name'

```
<br/>

EXAMPLE! Take a look at [`pose_parser`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/parsers/snapshot/pose_parser.py), and [`user_feelings_parser`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/parsers/snapshot/user_feelings_parser.py). <br/>

To add new parser, by class (parser that do require inner state), take the following easy and simple step: <br/>
Create a new file containig parser class, in the [`Snapshots Parsers`](https://github.com/AvivYaniv/Cortex/tree/master/cortex/parsers/snapshot) directory. <br/>
Parser object will be created once and then on each snapshot the parse function will be called.
To note a parser class, end it with `Parser` suffix, and add `parse` function.
<br/>
i.e.

```python
class YourParser:

    field = 'your_parser_field_name'

    def parse(self, snapshot):
        # Your code goes here
```
<br/>

EXAMPLE! Take a look at [`ColorImageParser`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/parsers/snapshot/color_image_parser.py), and [`DepthImageParser`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/parsers/snapshot/depth_image_parser.py). <br/>

<br/>

You can parser as a micro-service, by adding it to the [docker-compose.yml](https://github.com/AvivYaniv/Cortex/blob/master/docker-compose.yml) file, and defining the `RUN` environment variable to `PARSERS` and `PARSER` environment variable to `<your_parser_field_name>`. For more information please refer [How to add new micro-service](https://github.com/AvivYaniv/Cortex/blob/master/README.md#722-how-to-add-new-micro-service) in this document. <br/>

<br/>

### 5.3. MessageQueue

#### 5.3.1. MessageQueue Context Configuration
For the MessageQueue Framework, a dedicated dictionay-based file has been developed to configure ***any*** message-queue technology. <br/>

To configure contexts for a new message-queue technology, take the following easy and simple step: <br/>
Create in [MessageQueue Context](https://github.com/AvivYaniv/Cortex/tree/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/publisher_consumer/message_queue/context) directory, a dictionary-based file that starts with your message-queue technology name and ends with `_config.yaml`. <br/>

The header must be `message_queue`, to note a messsage-queue configuration file. <br/>

Header `message_queue` childrens are the services names. <br/>

Services childrens can be either [ publishers, consumers] or any other names defined under [ transmitter, receiver ] in [ RECIVERS_CATEGORIES_NAMES, TRANSMITTERS_CATEGORIES_NAMES] in [`MessageQueueContextFactory`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/publisher_consumer/message_queue/context/message_queue_context_factory.py), and from here it is possible to add any information required to initialize and configure your [ transmitter, receiver ]. <br/>

EXAMPLE! Take a look at [rabbitmq_config.yaml](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/publisher_consumer/message_queue/context/rabbitmq_config.yaml). <br/>

NOTE! To ensure configuration is as much useful as possible you can define in angle brackets fields that will be evaluated in runtime based on kwy-value arguments passed to [ `get_mq_category_contexts`, `get_mq_context` ] functions of [`MessageQueueContextFactory`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/publisher_consumer/message_queue/context/message_queue_context_factory.py). <br/>

To load message-queue context configuration, simply call either [ `get_mq_category_contexts`, `get_mq_context` ] functions of [`MessageQueueContextFactory`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/publisher_consumer/message_queue/context/message_queue_context_factory.py). <br/>

EXAMPLE! Take a look at [`ServerService`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/server/server_service.py), [`ParserService`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/parsers/parser_service.py), [`SaverService`](https://github.com/AvivYaniv/Cortex/blob/c12b3e9b6f648bc701381b2a7a399bae0bed3971/cortex/saver/saver_service.py). <br/>

#### 5.3.2. MessageQueue Driver
As stated above, it is possible to change to ***any*** message-queue technology. <br/>

To change for a new message-queue technology, take the following three easy and simple steps: <br/>
<br/>

&emsp; 1. 
Create context configuration file, as described in [MessageQueue Context Configuration](https://github.com/AvivYaniv/Cortex/blob/master/README.md#531-messagequeue-context-configuration) in this document. <br/>

<br/>

&emsp; 2. 
Add to [MessageQueue](https://github.com/AvivYaniv/Cortex/tree/master/cortex/publisher_consumer/message_queue) directory, a new class that inherits from [`MessageQueue`](https://github.com/AvivYaniv/Cortex/blob/4d1e0d34ab49841f3ccdffb530a9157ae28bde7e/cortex/publisher_consumer/message_queue/message_queue.py). To note a message-queue class, end it with `MessageQueue` suffix. <br/>


MessageQueue class must contain a `name` field and this would be the name for the message-queue technology.<br/>

MessageQueue class must contain the following functions:<br/>
`_default_hostname_resolution`			: That resolves default [ host, port ] parameters<br/>
`_health_check` 				: To indicate if connection with the message-queue can be established (consequative attempts will be made till it is available)<br/>
`_init_reciver` 				: To initialize a reciver, based on the `MessageQueue Context` member. <br/>
`_run_reciver` 					: To run a reciver. <br/>
`_run_transmitter` 				: To run a transmitter. <br/>
`_init_transmitter` 				: To initialize a transmitter, based on the `MessageQueue Context` member. <br/>
`_messege_queue_publish` 			: To publish messages. <br/>
`get_publish_function` 				: To return callback to message-queue publish function. <br/>
<br/>

<br/>

&emsp; 3. 
Add to [MessageQueue](https://github.com/AvivYaniv/Cortex/tree/master/cortex/publisher_consumer/message_queue) directory, scripts for message-queue installation (with `_install.sh` suffix) and message-queue shutdwon (with `_shutdown.sh` suffix), (shutdown script is used for testing only). <br/>

EXAMPLE! Take a look at [rabbitmq_install.sh](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/rabbitmq_install.sh), and [rabbitmq_shutdown.sh](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/rabbitmq_shutdown.sh). <br/>

<br/>

#### 5.3.3. MessageQueue Messages
A generic framework facilitates message-queue communication in easy and format-decoupled manner. <br/>

Current message-queue communication format is [JSON](https://en.wikipedia.org/wiki/JSON)-based. <br/>

Client-Server communication protocol format is being controlled in a *single* place (*yet can be changed for each couple of micro-services; [server-parser] or [parser-saver]*), based on default `messages_type` parameter resultion at [`MessageQueueMessages`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/messages/mq_messages.py). <br/>

NOTE! To change message-queue communication implementation format, simply create a new folder in [PublisherConsumer Messages](https://github.com/AvivYaniv/Cortex/tree/master/cortex/publisher_consumer/messages) directory, named after the new message-queue communication implementation format, and create in in classes for all the messages types that are in the [PublisherConsumer Messages](https://github.com/AvivYaniv/Cortex/tree/master/cortex/publisher_consumer/messages) directory. <br/>

EXAMPLE! Take a look at [JSON Messages](https://github.com/AvivYaniv/Cortex/tree/master/cortex/publisher_consumer/messages/json). <br/>


### 5.4. DataBase

#### 5.4.1. DataBase Driver
As stated above, it is possible to change to ***any*** database technology. <br/>

To change for a new message-queue technology, take the following three easy and simple steps: <br/>
<br/>

&emsp; 1. 
Create a new class that inherits from [`_DataBaseDriver`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/database/database_driver.py). To note a database class, end it with `DataBase` suffix. <br/>

DataBase class must contain a `name` field and this would be the name for the database technology.<br/>

DataBase class must contain the following functions:<br/>
`__init__`					: That initializes datase on specified [ host, port ] and sets logger. <br/>
`_clear` 					: To clear database (drop all tables), used for tests-only. <br/>
`_create` 					: To initialization of database, may include tables and triggers creation. <br/>
`create_entity` 				: To create new entity, based on `entity_name` with it's fields initialized according to key-value arguments. <br/>
`get_entity` 					: To retrive single entity, based on `entity_name` such as it's fields match to key-value arguments. <br/>
`get_entities` 					: To retrive multiple entities, based on `entity_name` such as their fields match to key-value arguments. <br/>
`get_entities_lazy` 				: To retrive multiple entities, in a lazy manner, based on `entity_name` such as their fields match to key-value arguments. <br/>
`update_entity` 				: To update single entity, based on `entity_name`, based on it's ID [ `id_name`, `id_value` ], such as it's new fields values match to key-value arguments. <br/>
`has_entity` 					: To indicate if entity of type `entity_name`, exists such as key-value arguments are matched. <br/>
<br/>

<br/>

&emsp; 2. 
Add to [DataBase](https://github.com/AvivYaniv/Cortex/tree/master/cortex/database) directory, scripts for database installation (with `_install.sh` suffix) and database shutdwon (with `_shutdown.sh` suffix), (shutdown script is used for testing only). <br/>

EXAMPLE! Take a look at [mongodb_install.sh](https://github.com/AvivYaniv/Cortex/blob/master/cortex/database/mongodb_install.sh), and [mongodb_shutdown.sh](https://github.com/AvivYaniv/Cortex/blob/master/cortex/database/mongodb_shutdown.sh). <br/>

### 5.5. API

#### 5.5.1. API Format
The API server results are in [JSON](https://en.wikipedia.org/wiki/JSON) format, but format can be costumized easily. <br/>

To change API results format (AKA [marshal](https://en.wikipedia.org/wiki/Marshalling_(computer_science))), take the following three easy and simple step: <br/>
Create a new class under the [Marshal](https://github.com/AvivYaniv/Cortex/tree/master/cortex/api/marshal) directory. To note a marshal class, end it with `Marshal` suffix.  <br/> 

Marshal class must contain a `type` field and this would be the name for the marshal format.<br/>

Marshal class must contain the following function:<br/>
`marshal`					: That gets a dictionary and returns it formatted according to `marshal` format. <br/>

EXAMPLE! Take a look at [JSON Marshal](https://github.com/AvivYaniv/Cortex/blob/master/cortex/api/marshal/json_marshal.py). <br/>

<br/> 

@@@ TODO CONTINUE :

#### 5.5.2. API URLs
The API server utilities [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/). <br/>
INFO! The API URLs format mentioned in API service easily support any other web-framework as described in [API URLs](https://github.com/AvivYaniv/Cortex/blob/master/README.md#552-api-urls) in this document. <br/>

@@@ TODO CONTINUE :

### 5.6. GUI
@@@ TODO CONTINUE :

#### 5.6.1. Bar Charts
@@@ TODO CONTINUE :

#### 5.6.2. Multiline Graphs
@@@ TODO CONTINUE :

## 6. Tests
@@@ TODO CONTINUE :

### 6.1. Test tools
@@@ TODO CONTINUE :

## 7. Additional Information
### 7.1. Scripts

The `scripts` folder contains the following useful scripts:

1. [ `client1.sh`, `client2.sh` ] : For client emulation as sanity-check.
2. `docs.sh` : For automatic-documentation, so changes in documentation will take effect immideiatly.
3. `dos2unix.sh` : To convert `.sh` files in the project to unix [end-of-line](https://en.wikipedia.org/wiki/Newline), for users of `Microsoft` oriented OSs.
4. `install.sh` : For project installation, as covered in the [Installation](https://github.com/AvivYaniv/Cortex/blob/master/README.md#installation) chapter in this document.
5. `presequites.sh` : For project presequites installation, as covered in the [Installation](https://github.com/AvivYaniv/Cortex/blob/master/README.md#installation) chapter in this document.
6. `remove_containers.sh` : To clear all docker containers and images.
7. `restore-pipeline.sh` : To bring up docker containers, after stopped (i.e. by `stop-pipeline.sh`).
8. `run_container.sh` : This script is for internal usage, and used to run specific container by docker-compose.
9. `run-pipeline.sh` : To run project, as covered in the [Installation](https://github.com/AvivYaniv/Cortex/blob/master/README.md#installation) chapter in this document.
9. `stop-pipeline.sh` : To stop project containers.
10. `wait-for-it.sh` : Mainly for internal usage, used by docker to wait for micro-service to be available on specific port.

### 7.2. Docker
#### 7.2.1. Docker startup

Project startup uses docker-compose to bring up micro-services. <br/>

Upon `run-pipeline.sh` script execution, the following actions will take place:

1. ~Previous docker containers and images are deleted.~ (Uncomment in script to activate) <br/>
2. Micro-services containers are built according to `docker-compose.yml` based on `Dockerfile` configuration. <br/>
2.1. Container image is created. <br/>
2.2. Project files are copied to image. <br/>
2.3. The `run_container.sh` script is executed, to create new container: <br/>
2.3.1. Project requirements are installed on container. <br/>
2.3.2. Container is booted according to `boot_container.py` script: <br/>
2.3.2.1. Based on `RUN` environment variable value, micro-service is package located. <br/>
2.3.2.2. Micro-service package's `boot_container.py` script is executed and runs it. <br/>

#### 7.2.2. How to add new micro-service

@@@ TODO CONTINUE :
