
import os
import sys

from cortex.database.database_runner import run_database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

import pytest

import multiprocessing

from tests.test_constants import DEFAULT_INITIALIZATION_DURATION

import tests.saver.pytest_shared as pytest_shared 
pytest_shared.init_shared_variables()

def pytest_sessionstart(session):
    database_proccess = multiprocessing.Process(target=run_database)
    database_proccess.start()
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    # pytest_shared.shared_dictionary['database_proccess'] = database_proccess 
    
def pytest_sessionfinish(session, exitstatus):
    # pytest_shared.shared_dictionary['database_proccess'].kill()
    pass
