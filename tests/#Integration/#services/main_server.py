
# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.server import run_server


if "__main__" == __name__:
    file    = 'sample.mind.gz'
    host, port = '127.0.0.1', '8000'
    run_server(host, port)    

