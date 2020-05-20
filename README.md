![build status](https://api.travis-ci.com/AvivYaniv/Cortex.svg?branch=master)
![coverage](https://codecov.io/gh/AvivYaniv/Cortex/branch/master/graph/badge.svg)
![docs](https://readthedocs.org/projects/braincomputerinterface/badge/?version=latest)

# Cortex

Cortex is brain-comuter-interface *ultra **flexibale** and **durable*** project, which enabels to upload and view users telemetry data. 
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
5. [Flexability and SOLIDness](https://github.com/AvivYaniv/Cortex/blob/master/README.md#5-flexability-and-solidness) <br/>
5.1. Client <br/>
5.1.1. File Readers <br/>
5.1.2. Mind File Formats <br/>
5.2. Parsers <br/>
5.2.1. Adding Parser <br/>
5.3. MessageQueue <br/>
5.3.1. MessageQueue Context Configuration <br/>
5.3.2. MessageQueue Driver <br/>
5.4. API <br/>
5.4.1. API Format <br/>
5.4.2. API URLs <br/>
5.5. GUI <br/>
5.5.1. Bar Charts <br/>
5.5.2. Multiline Graphs <br/>
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
The API server utilities [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/). <br/>
INFO! The API server results are in [JSON](https://en.wikipedia.org/wiki/JSON) format, but format can be costumized easily as described in @@@ TODO LINK @@@ <br/>
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

NOTE! The terms [ transmitter, receiver ] and [ publisher, consumer ] will be used interchangeably, yet the latter are concrete instances for the [ transmitter, receiver ] concep. <br/>

The following UML diagram depicts the main components: <br/>
@@@ TODO : LINK @@ <br/>

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

3. MessageQueue Publishers: <br/>
The MessageQueue Publisher can be run either: <br/>
1. In a dedicated thread as [`MessageQueuePublisherThread`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/publisher/message_queue_publisher_thread.py) (to handle [IO Event Loop](https://en.wikipedia.org/wiki/Event_loop)). <br/>
2. In the same thread as [`MessageQueuePublisher`](https://github.com/AvivYaniv/Cortex/blob/master/cortex/publisher_consumer/message_queue/publisher/message_queue_publisher.py). <br/>

IMPORTANT! The MessageQueue Publisher activates, yet decoupled from, the concrete technology implementation; which is dynamically loaded based on the `message_queue_type` parameter and initialized based on a `MessageQueueContext` which is passed with the `message_queue_context` parameter. <br/>

4. MessageQueue Consumers: <br/>
5. MessageQueue Runner: <br/>

### 4.2. DataBase
@@@ TODO CONTINUE : 

## 5. Flexability and [SOLIDness](https://en.wikipedia.org/wiki/SOLID)

The Cortex project is built to be flexibale for modification and customizations.

> "Make the easy things easy, and the hard things possible" ~ Larry Wall (Programming Perl, 2nd Edition (1996), by Larry Wall, Tom Christiansen and Randal Schwartz)

### 5.1. Client
@@@ TODO CONTINUE : 

#### 5.1.1. File Readers
@@@ TODO CONTINUE : 

#### 5.1.2. Mind File Formats
@@@ TODO CONTINUE : 

### 5.2. Parsers
@@@ TODO CONTINUE :

#### 5.2.1. Adding Parser
@@@ TODO CONTINUE :

### 5.3. MessageQueue
@@@ TODO CONTINUE : 

#### 5.3.1. MessageQueue Context Configuration
@@@ TODO CONTINUE :

#### 5.3.2. MessageQueue Driver
@@@ TODO CONTINUE :

### 5.4. API
@@@ TODO CONTINUE : 

#### 5.4.1. API Format
@@@ TODO CONTINUE :

#### 5.4.2. API URLs
@@@ TODO CONTINUE :

### 5.5. GUI
@@@ TODO CONTINUE :

#### 5.5.1. Bar Charts
@@@ TODO CONTINUE :

#### 5.5.2. Multiline Graphs
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
