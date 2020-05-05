import sys

import click

import cortex.api

import logging
from cortex.logger import _LoggerLoader
from cortex.api.api import run_api_server

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

@click.group()
@click.version_option(cortex.api.version)
def main():
    pass

@main.command()
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
@click.option('-d', '--database', default='')
def run_server(host, port, database):
    """
    Runs API server that can handle requests
    """
    run_api_server(host, port, database)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.api', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        