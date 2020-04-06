import sys

import click

import cortex.server

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
@click.argument('data_dir', type=str)
def run_server(host, port, data_dir):
    """
    Starts a server to which samples can be uploaded to with `upload_sample`
    """
    cortex.server.run_server(host, port, data_dir)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.server', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        