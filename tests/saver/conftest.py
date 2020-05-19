
import os
import sys

from cortex.database.database_runner import run_database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

import pytest

import multiprocessing

from tests.test_constants import DEFAULT_INITIALIZATION_DURATION

import tests.saver.pytest_shared as pytest_shared 

def pytest_sessionstart(session):
    pytest_shared['database_proccess'] = 'sabich'    
    #pytest.database_proccess = multiprocessing.Process(target=run_database)
    #pytest.database_proccess.start()
    #time.sleep(DEFAULT_INITIALIZATION_DURATION)
    
def pytest_sessionfinish(session, exitstatus):
    #global _database_proccess
    pytest_shared['database_proccess'].kill()
