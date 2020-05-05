import sys

import click

import requests

import cortex.cli

from cortex.api.api_urls import *

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

def do_api_request(url_format, host, *args):
    requst_url               =   get_api_url(url_format, host).format(*args)    
    requst_result            =   requests.get(requst_url)
    return requst_result

def fetch_api_request_text(url_format, host, *args):    
    return do_api_request(url_format, host, *args).text

# Click Methods Section
@click.group()
@click.version_option(cortex.cli.version)
def main():
    pass

@main.command()
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
def get_users(host, port):
    """
    Gets all users
    """
    api_host = build_api_host_name(host, port)
    result = fetch_api_request_text(API_URL_FORMAT_GET_ALL_USERS, api_host)
    print(result)

@main.command()
@click.argument('user_id', type=str)
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
def get_user(user_id, host, port):
    """
    Gets users details
    """    
    api_host = build_api_host_name(host, port)
    result = fetch_api_request_text(API_URL_FORMAT_GET_USER, api_host, user_id)
    print(result)

@main.command()
@click.argument('user_id', type=str)
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
def get_snapshots(user_id, host, port):
    """
    Gets users snapshots
    """    
    api_host = build_api_host_name(host, port)
    result = fetch_api_request_text(API_URL_FORMAT_GET_ALL_USER_SNAPSHOTS, api_host, user_id)
    print(result)

@main.command()
@click.argument('user_id', type=str)
@click.argument('snapshot_uuid', type=str)
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
def get_snapshot(user_id, snapshot_uuid, host, port):
    """
    Gets users snapshot
    """    
    api_host = build_api_host_name(host, port)
    result = fetch_api_request_text(API_URL_FORMAT_GET_USER_SNAPSHOT, api_host, user_id, snapshot_uuid)
    print(result)
    
@main.command()
@click.argument('user_id', type=str)
@click.argument('snapshot_uuid', type=str)
@click.argument('result_name', type=str)
@click.option('-h', '--host', default='')
@click.option('-p', '--port', default='')
@click.option('-s', '--save', default='')
def get_result(user_id, snapshot_uuid, result_name, host, port, save):
    """
    Gets users snapshot's result
    """    
    api_host = build_api_host_name(host, port)
    if save:
        result = do_api_request(API_URL_FORMAT_GET_RESULT_DATA, api_host, user_id, snapshot_uuid, result_name)
        with open(save, 'wb') as f:
            f.write(result.content) 
    else:
        result = fetch_api_request_text(API_URL_FORMAT_GET_RESULT, api_host, user_id, snapshot_uuid, result_name)
        print(result)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.cli', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        