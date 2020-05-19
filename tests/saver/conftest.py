
import os
import sys

from cortex.database.database_runner import run_database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

import pytest

import multiprocessing

from tests.test_constants import DEFAULT_INITIALIZATION_DURATION

global _database_proccess

def pytest_sessionstart(session):
    global _database_proccess
    _database_proccess = multiprocessing.Process(target=run_database)
    _database_proccess.start()
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    
def pytest_sessionfinish(session, exitstatus):
    global _database_proccess
    _database_proccess.kill()
