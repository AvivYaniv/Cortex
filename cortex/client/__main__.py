import sys

import click

import cortex.client

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

@click.group()
@click.version_option(cortex.client.version)
def main():
    pass

@main.command()
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
@click.argument('file', type=str)
def upload_sample(host, port, file):
    """
    Sends to the server user's sample file; user information & snapshots
    """
    cortex.client.upload_sample(host, port, file)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.client', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        