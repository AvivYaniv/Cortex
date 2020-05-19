![build status](https://api.travis-ci.com/AvivYaniv/Cortex.svg?branch=master)
![coverage](https://codecov.io/gh/AvivYaniv/Cortex/branch/master/graph/badge.svg)

# Cortex

Cortex is brain-comuter-interface ultra flexibale and durable project, which enabels to upload and view users telemetry data. 
<br/>See [full documentation](https://braincomputerinterface.readthedocs.io/en/latest/).

Telemetry data currently contains snapshots of:
1. User feelings: consists of the following [hunger, thirst, exhaustion, happiness], and ranged between [-1,1].
2. [Pose](https://en.wikipedia.org/wiki/Pose_(computer_vision)): a computer-vision concept to determine object's position (user) and orientation relative to some coordinate system, and consists of two vectors: [ Translation, Rotation ].
3. Color image: shows what the user sees.
4. Depth image: shows 'heatmap' of user distance relatively to objects that are in front of the user.

Cortex project is the final project of [Advanced System Design](https://advanced-system-design.com/) at Tel-Aviv Univeristy by [Dan Gittik](https://dan-gittik.com/).

## Table Of Contents

1. Architecture <br/>
2. Installation <br/>
3. Modules <br/>
3.1. Client <br/>
3.2. Server <br/>
3.3. Parsers <br/>
3.4. Savers <br/>
3.5. API <br/>
3.6. GUI <br/>
3.7. CLI <br/>
4. Frameworks <br/>
4.1. MessageQueue <br/>
4.2. DataBase <br/>
5. Flexability and SOLIDness <br/>
6. Tests <br/>
6.1. Test tools <br/>
7. Additional Information <br/>
7.1. Scripts <br/>
7.2. Docker <br/>
7.2.1. Docker startup <br/>
7.2.2. How to add new micro-service <br/>

## Architecture

The Cortex project contains of client that communicates to server user's telemetry data, as matter of [lifelogging](https://en.wikipedia.org/wiki/Lifelog).

The server passes the snapshot messages to a message-queue. <br/>
Parser micro-services consume from the message-queue the raw snapshots and push to the message-queue the parsed results. <br/>
Savers pull from the message-queue the parsed results, in a load-balanced manner, and save them to the database.

Project also provides a GUI server to which users can connect to view telemetry data.

Other micro-services that are included are API to pull data from the database and CLI to run specific services.

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
Client used to upload a `mind` file to server, which is a presentation of telemetry snapshots <br/>
1. API:
    ```python
    >>> from cortex.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to host:port
    ```
2. CLI:
    ```sh
    $ python -m cortex.client upload-sample \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
	…
    ```
<br/>
Issues & Actions:<br/>
1. File not found : client will write error message to user. <br/>
2. Communication error : client will exit graciously. <br/>
3. Server is unavailable : client will retray to connect for few times, and then exit if failed to connect. <br/>
<br/>

@@@ TODO CONTINUE : ### 3.2. Server
@@@ TODO CONTINUE : ### 3.3. Parsers
@@@ TODO CONTINUE : ### 3.4. Savers
@@@ TODO CONTINUE : ### 3.5. API
@@@ TODO CONTINUE : ### 3.6. GUI
@@@ TODO CONTINUE : ### 3.7. CLI
@@@ TODO CONTINUE : ## 4. Frameworks
@@@ TODO CONTINUE : ### 4.1. MessageQueue
@@@ TODO CONTINUE : ### 4.2. DataBase


## Flexability and [SOLIDness](https://en.wikipedia.org/wiki/SOLID)

The `cortex` project is built to be flexibale for modification and customizations.

> "Make the easy things easy, and the hard things possible" ~ Larry Wall (Programming Perl, 2nd Edition (1996), by Larry Wall, Tom Christiansen and Randal Schwartz)

## Server

## Adding parsers

By adding parser you can manipulate and save in the snapshot recived on the server.
To add parser, all you have to do is to create a file under the `parsers` sub-package with parser function or class.

You can note the client that your parser works on specific field, so client would know about it in `Config` message.

Parser function:
Parser function is used for parsing data that does not require a state.
To note a parser function, end it with `_parser` suffix.
<br/>i.e.
```python
def your_parser(context, snapshot):
    # Your code goes here
my_parser.field = 'your_parser_field_name'

```

Parser class:
Parser class is used for parsing data that requires a state.
Parser object will be created once and then on each snapshot the parse function will be called.
To note a parser class, end it with `Parser` suffix, and add `parse` function.
<br/>i.e.
```python
class YourParser:

    field = 'your_parser_field_name'

    def parse(self, context, snapshot):
        # Your code goes here
```

## Client Personalization for Programmers

## Adding readers

By adding reader you can add files that serialize user information and snapshot, in your prefered manner.
To add parser, all you have to do is to create a file under the `readers` sub-package with reader class.

Reader class:
Reader class must contain a `version` field and this would be the name for reading files according to this reader.

Reader class must contain the following functions:
`__init__`					: That recives the file path to be read	
`read_user_information` 	: To read user information
`read_snapshot` 			: To read snapshots

The file will be opened, user information will be read and then the snapshots.

To note a reader class, end it with `Reader` suffix.
<br/>i.e.
```python
class YourReader:

	version = 'your_reader_name'

	def __init__(self, file_path):
		# Your code goes here

	def read_user_information(self):
		# Your code goes here

	def read_snapshot(self):
		# Your code goes here
```

@@@ TODO CONTINUE : ## 6. Tests
@@@ TODO CONTINUE : ### 6.1. Test tools

## Additional Information
### Scripts

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

### Docker
#### Docker startup

Project startup uses docker-compose to bring up micro-services. <br/>

Upon `run-pipeline.sh` script execution, the following actions will take place:

1. Previous docker containers and images are deleted. <br/>
2. Micro-services containers are built according to `docker-compose.yml` based on `Dockerfile` configuration. <br/>
2.1. Container image is created. <br/>
2.2. Project files are copied to image. <br/>
2.3. The `run_container.sh` script is executed, to create new container: <br/>
2.3.1. Project requirements are installed on container. <br/>
2.3.2. Container is booted according to `boot_container.py` script: <br/>
2.3.2.1. Based on `RUN` environment variable value, micro-service is package located. <br/>
2.3.2.2. Micro-service package's `boot_container.py` script is executed and runs it. <br/>

@@@ TODO CONTINUE : #### How to add new micro-service
