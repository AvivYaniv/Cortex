![build status](https://api.travis-ci.com/AvivYaniv/Cortex.svg?branch=master)
![coverage](https://codecov.io/gh/AvivYaniv/Cortex/branch/master/graph/badge.svg)

# Cortex

Package for brain-comuter-interface, enabels to upload and view users thoughts. 
<br/>See [full documentation](https://braincomputerinterface.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:AvivYaniv/Cortex.git
    ...
    $ cd Cortex/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [Cortex] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `cortex` package provides a command-line interface:

```sh
$ python -m cortex
Usage: cortex [OPTIONS] COMMAND [ARGS]...

Options:
  --version        Show the version and exit.
  -q, --quiet
  -t, --traceback
  --help           Show this message and exit.

Commands:
  run-server
  run-webserver
  upload-sample

```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `run-server` command:
	This command starts a server to which sample files can be uploaded to with the `upload_sample` command
	<br/> Usage: run-server [address] [data_dir]

```sh
$ python -m cortex run_server '127.0.0.1:8000' 'data'

```

The CLI further provides the `run-webserver` command:
	This command starts a server to which shows users thoughts
	<br/> Usage: run-webserver [address] [data_dir]

```sh
$ python -m cortex run_webserver '127.0.0.1:8000' 'data'

```

The CLI further provides the `upload-sample` command:
	This command sends to the server user's sample file
	File can be either zipped (*.gz) or raw (*.mind)
	Versions suppored: binary or protobuf
	<br/> Usage: upload-sample [address] [file] [version]

```sh
$ python -m cortex client_run '127.0.0.1:8000' 'sample.mind' 'protobuf'

```

## Advanced Personalization for Programmers

The `cortex` package provides the ability to further personalized handling of files and parsers.

## Server Personalization for Programmers

## Adding parsers

By adding parser you can manipulate and save in the snapshot recived on the server.
To add parser, all you have to do is to create a file under the `parsers` sub-package with parser function or class.

You can note the client that your parser works on specific field, so client would know about it in `Config` message.

Parser function:
Parser function is used for parsing data that does not require a state.
To note a parser function, end it with `_parser` suffix.
<br/>i.e.
```
def your_parser(context, snapshot):
    # Your code goes here
my_parser.field = 'your_parser_field_name'

```

Parser class:
Parser class is used for parsing data that requires a state.
Parser object will be created once and then on each snapshot the parse function will be called.
To note a parser class, end it with `Parser` suffix, and add `parse` function.
<br/>i.e.
```
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
```
class YourReader:

	version = 'your_reader_name'

	def __init__(self, file_path):
		# Your code goes here

	def read_user_information(self):
		# Your code goes here

	def read_snapshot(self):
		# Your code goes here
```
