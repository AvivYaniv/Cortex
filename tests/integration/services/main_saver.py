
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.saver import run_saver_service

if "__main__" == __name__:
    run_saver_service()   
