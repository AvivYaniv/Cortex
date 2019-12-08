![build status](https://api.travis-ci.com/AvivYaniv/Cortex.svg?branch=master)
![coverage](https://codecov.io/gh/AvivYaniv/Cortex/branch/master/graph/badge.svg)

# Cortex

Package for brain-comuter-interface, enabels to upload and view users thoughts. 
<br/>See [full documentation](https://advancedsystemdesignproject.readthedocs.io/en/latest/).

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
<br/>Usage: cortex [OPTIONS] COMMAND [ARGS]...

Options:
  --version        Show the version and exit.
  -q, --quiet
  -t, --traceback
  --help           Show this message and exit.

Commands:
  run-server
  run-webserver
  upload-thought

```

All commands accept the `-q` or `--quiet` flag to suppress output, and the `-t`
or `--traceback` flag to show the full traceback when an exception is raised
(by default, only the error message is printed, and the program exits with a
non-zero code).

The CLI provides the `run-server` command:
	This command starts a server to which thoughts can be uploaded to with the `upload_thought` command
	<br/>Usage: run-server [address] [data_dir]

```sh
$ python -m cortex run-server '127.0.0.1:8000' 'data'

```

The CLI further provides the `run-webserver` command:
	This command starts a server to which shows users thoughts
	<br/>Usage: run-webserver [address] [data_dir]

```sh
$ python -m cortex run-webserver '127.0.0.1:8000' 'data'

```

The CLI further provides the `upload-thought` command:
	This command sends to the server user's thought
	<br/>Usage: upload-thought [address] [user_id] [thought]

```sh
$ python -m cortex run-webserver '127.0.0.1:8000' 123 'sabich'

```
