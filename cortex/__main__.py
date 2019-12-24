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
    
@main.command()
@click.argument('file', type=str)
def read(file):
    """
    Reads a sample file
    """
    log(cortex.read(file))

# run_webserver(address, data_dir)
@main.command()
@click.argument('address', type=str)
@click.argument('data_dir', type=str)
def run_webserver(address, data_dir):
    """
    Starts a server to which shows users thoughts
    """
    log(cortex.run_webserver(address, data_dir))

@main.command()
@click.argument('address', type=str)
@click.argument('data_dir', type=str)
def server_run(address, data_dir):
    """
    Starts a server to which smaples can be uploaded to with `upload_sample`
    """
    log(cortex.run_server(address, data_dir))

@main.command()
@click.argument('address', type=str)
@click.argument('file', type=str)
@click.argument('version', type=str)
def client_run(address, file, version):
    """
    Sends to the server user's sample file; user information & snapshots
    """
    log(cortex.upload_sample(address, file, version))

if __name__ == '__main__':
    try:
        main(prog_name='cortex', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
        