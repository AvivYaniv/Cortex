
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.api.api_server import run_api

if "__main__" == __name__:
    run_api()
