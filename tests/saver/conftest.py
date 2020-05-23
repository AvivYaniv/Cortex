
import os
import sys

from cortex.database.database_runner import run_database
from cortex.database.database_runner import stop_database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

import pytest

import multiprocessing

from tests.test_constants import DEFAULT_INITIALIZATION_DURATION
from tests.test_constants import DEFAULT_SHUTDOWN_DURATION
from tests.test_constants import is_on_ci_environment

import tests.saver.pytest_shared as pytest_shared 
pytest_shared.init_shared_variables()

def pytest_sessionstart(session):
    database_proccess = multiprocessing.Process(target=run_database)
    database_proccess.start()
    time.sleep(DEFAULT_INITIALIZATION_DURATION)
    pytest_shared.shared_dictionary['database_proccess'] = database_proccess 
    
def pytest_sessionfinish(session, exitstatus):
    if not is_on_ci_environment():
        pytest_shared.shared_dictionary['database_proccess'].kill()
        database_shutdown_proccess = multiprocessing.Process(target=stop_database)
        database_shutdown_proccess.start()
        database_shutdown_proccess.join(DEFAULT_SHUTDOWN_DURATION)
        database_shutdown_proccess.kill()
