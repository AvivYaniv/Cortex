import os

from cortex.server import run_server

from cortex.client import upload_sample

from cortex.readers.reader_versions import ReaderVersions

print("Hello Sabich! ")

# Messages Section
UNKNOWN_COMMAND_TO_RUN_ERROR_MESSAGE    =   'Unknown command to run, environment variable is illegal'
RUNNING_COMMAND_INFO_MESSAGE            =   'Running command...'

# Functions Section
def run_client():
    file_path    	= 	'sample.mind.gz'
    host, port 		= 	'127.0.0.1', '8000'
    upload_sample(host, port, file_path=file_path, version=ReaderVersions.PROTOBUFF)

def run_server():
    host, port 		= 	'127.0.0.1', '8000'
    run_server(host, port)

# Variables Section
RUN_FUNCTIONS_DICTIONARY =      \
    {                           \
        'SERVER' : run_server,  \
        'CLIENT' : run_client   \
    }

if "__main__" == __name__:
    run_command = os.environ['RUN']
    
    if (run_command not in RUN_FUNCTIONS_DICTIONARY):
        print(UNKNOWN_COMMAND_TO_RUN_ERROR_MESSAGE)
    else:
        print(RUNNING_COMMAND_INFO_MESSAGE)
        RUN_FUNCTIONS_DICTIONARY[run_command]()
