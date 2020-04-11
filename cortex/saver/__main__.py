import sys

import click

import cortex.saver
import cortex.saver.saver

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

@click.group()
@click.version_option(cortex.saver.version)
def main():
    pass

@main.command()
@click.option('-d', '--database', default='')
@click.argument('message', type=str)
def saver(db_url, message):
    """
    Invokes saver to save a message as retrieved from a message queue
    """
    saver = cortex.saver.saver.Saver(db_url)
    saver.save(message)

@main.command()
@click.option('-d', '--database', default='')
@click.option('-mq', '--message_queue', default='')
def run_saver(db_url, mq_url):
    """
    Runs a saver as a service 
    which works with a message queue indefinitely; 
    saver subscribes to all the relevant topics it is capable of consuming 
    and saving to the database.
    """
    cortex.saver.saver.run_saver(db_url, mq_url)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.saver', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        