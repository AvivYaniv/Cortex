import os
import sys
import traceback

import click

import cortex


class Log:
    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info(): # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()

@click.group()
@click.version_option(cortex.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback
    
# run_server(address, data_dir)
@main.command()
@click.argument('file', type=str)
def read(file):
    """
    Reads a sample file
    """
    log(cortex.read(file))

# run_server(address, data_dir)
@main.command()
@click.argument('address', type=str)
@click.argument('data_dir', type=str)
def run_server(address, data_dir):
    """
    Starts a server to which thoughts can be uploaded to with `upload_thought`
    """
    log(cortex.run_server(address, data_dir))

# upload_thought(address, user_id, thought)
@main.command()
@click.argument('address', type=str)
@click.argument('user_id', type=int)
@click.argument('thought', type=str)
def upload_thought(address, user_id, thought):
    """
    Sends to the server user's thought
    """
    log(cortex.upload_thought(address, user_id, thought))

# run_webserver(address, data_dir)
@main.command()
@click.argument('address', type=str)
@click.argument('data_dir', type=str)
def run_webserver(address, data_dir):
    """
    Starts a server to which shows users thoughts
    """
    log(cortex.run_webserver(address, data_dir))


if __name__ == '__main__':
    try:
        main(prog_name='cortex', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
        