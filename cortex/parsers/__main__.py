import sys

import click

import cortex.parsers

from cortex.parsers.parser import run_parser
from cortex.parsers.parser import MessageParser

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

@click.group()
@click.version_option(cortex.parsers.version)
def main():
    pass

@main.command()
@click.argument('parser_type', type=str)
@click.argument('raw_snapshot_message_path', type=str)
def parse(parser_type, raw_snapshot_message_path):
    """
    Accepts a parser name and a path to some raw data, 
    and prints the result, as published to the message queue 
    (optionally redirecting it to a file).
    """
    message_parser  = MessageParser(parser_type)
    result          = message_parser.parse_message(raw_snapshot_message_path)
    return result

@main.command()
@click.argument('parser_type', type=str)
@click.argument('mq_url', type=str)
def run_parser(parser_type, mq_url):
    """
    Starts a parser of the given type and publishes parsed output to message-queue
    """
    run_parser(parser_type, mq_url)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.parsers', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        