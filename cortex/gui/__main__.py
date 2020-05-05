import sys

import click

import cortex.gui

from cortex.gui.gui_server import run_gui_server  

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Click Methods Section
@click.group()
@click.version_option(cortex.gui.version)
def main():
    pass

@main.command()
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
@click.option('-H', '--api-host', default='')
@click.option('-P', '--api-port', default='')
def run_server(host, port, api_host, api_port):
    """
    Runs GUI server
    """
    run_gui_server(host, port, api_host, api_port)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.gui', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        