
import os
import sys

from cortex.database.database_runner import run_database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

import pytest

def pytest_sessionstart(session):
    run_database()

def pytest_sessionfinish(session, exitstatus):
    pass
