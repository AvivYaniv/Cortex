import sys

import click

import json
import requests

import cortex.cli

from cortex.api.api_urls import *

import logging
from cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Methods Section
def do_api_request(url_format, *args):
    requst_url               =   get_api_url(url_format).format(*args)    
    requst_result            =   requests.get(requst_url)
    return requst_result

def fetch_api_request(url_format, *args):    
    return do_api_request(url_format, *args).text

# Click Methods Section
@click.group()
@click.version_option(cortex.cli.version)
def main():
    pass

@main.command()
def get_users():
    """
    Gets all users
    """
    result = fetch_api_request(API_URL_FORMAT_GET_ALL_USERS)
    print(result)

@main.command()
@click.argument('user_id', type=str)
def get_user(user_id):
    """
    Gets users details
    """    
    result = fetch_api_request(API_URL_FORMAT_GET_USER, user_id)
    print(result)

@main.command()
@click.argument('user_id', type=str)
def get_snapshots(user_id):
    """
    Gets users snapshots
    """    
    result = fetch_api_request(API_URL_FORMAT_GET_ALL_USER_SNAPSHOTS, user_id)
    print(result)

@main.command()
@click.argument('user_id', type=str)
@click.argument('snapshot_uuid', type=str)
def get_snapshot(user_id, snapshot_uuid):
    """
    Gets users snapshot
    """    
    result = fetch_api_request(API_URL_FORMAT_GET_USER_SNAPSHOT, user_id, snapshot_uuid)
    print(result)
    
@main.command()
@click.argument('user_id', type=str)
@click.argument('snapshot_uuid', type=str)
@click.argument('result_name', type=str)
@click.option('-s', '--save', default='')
def get_result(user_id, snapshot_uuid, result_name, save):
    """
    Gets users snapshot's result
    """    
    if save:
        result = do_api_request(API_URL_FORMAT_GET_RESULT_DATA, user_id, snapshot_uuid, result_name)
        with open(save, 'wb') as f:
            f.write(result.content) 
    else:
        result = fetch_api_request(API_URL_FORMAT_GET_RESULT, user_id, snapshot_uuid, result_name)
        print(result)

if __name__ == '__main__':
    try:
        main(prog_name='cortex.cli', obj={})
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
        