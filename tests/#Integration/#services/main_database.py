
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.database.database_runner import run_database

if "__main__" == __name__:
    run_database()
