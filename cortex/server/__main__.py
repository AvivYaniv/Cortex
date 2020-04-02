import sys

import click

import cortex.server

import logging
from cortex.logger import LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = LoggerLoader()
logger_loader.load_log_config()

@click.group()
@click.version_option(cortex.client.version)
def main():
    pass

@main.command()
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default='8000')
@click.argument('data_dir', type=str)
def run_server(host, port, data_dir):
    """
    Starts a server to which smaples can be uploaded to with `upload_sample`
    """
    cortex.server.run_server(host, port, data_dir)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.server', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        