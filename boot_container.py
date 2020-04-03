import os
import sys

# Constants Section
CONTAINER_NAME_ENVIRONMENT_VARIABLE                 =   'RUN'      
PROJECT_BASE_DIRECTORY                              =   'cortex'
CONTAINER_BOOT_FILE_NAME                            =   'boot_container.py'

# Messages Section
NO_CONTAINER_SPECIFIED_ERROR_MESSAGE                =   'ERROR: No container specified in environment variable ' + CONTAINER_NAME_ENVIRONMENT_VARIABLE 
CONTAINER_DIRECTORY_NOT_FOUND_ERROR_MESSAGE_FRMT    =   'ERROR: Container directory {} not found'
CONTAINER_BOOT_FILE_NOT_FOUND_ERROR_MESSAGE_FRMT    =   'ERROR: Container boot file {} not found'
BOOTING_CONTAINER_INFO_MESSAGE                      =   'Booting container...'

class ERROR_CODES:
    NO_ERROR                        =   0
    NO_NO_CONTAINER_SPECIFIED       =   -1
    CONTAINER_DIRECTORY_NOT_FOUND   =   -2
    CONTAINER_BOOT_FILE_NOT_FOUND   =   -3


def get_container_path(container_name):
    return os.path.join(PROJECT_BASE_DIRECTORY, container_name.lower())

def get_container_boot_file_path(container_path, container_boot_file_name=CONTAINER_BOOT_FILE_NAME):
    return os.path.join(container_path, container_boot_file_name)

if "__main__" == __name__:
    # Validating container has been specified
    if CONTAINER_NAME_ENVIRONMENT_VARIABLE not in os.environ:
        print(NO_CONTAINER_SPECIFIED_ERROR_MESSAGE)
        sys.exit(ERROR_CODES.NO_NO_CONTAINER_SPECIFIED)
        
    # Fetching environment variable to determine which code to run
    container_name = os.environ[CONTAINER_NAME_ENVIRONMENT_VARIABLE]
    
    # Building container path
    container_path = get_container_path(container_name)
    
    # If container folder dosen't exist
    if (not os.path.isdir(container_path)):
        print(CONTAINER_DIRECTORY_NOT_FOUND_ERROR_MESSAGE_FRMT.format(container_path))
        sys.exit(ERROR_CODES.CONTAINER_DIRECTORY_NOT_FOUND)
    
    # Building container boot file path
    container_boot_file_path = get_container_boot_file_path(container_path)
    
    # If container folder dosen't exist
    if (not os.path.isfile(container_boot_file_path)):
        print(CONTAINER_BOOT_FILE_NOT_FOUND_ERROR_MESSAGE_FRMT.format(container_boot_file_path))
        sys.exit(ERROR_CODES.CONTAINER_BOOT_FILE_NOT_FOUND)
    
    # Booting container
    print(BOOTING_CONTAINER_INFO_MESSAGE)
    exec(open(container_boot_file_path).read())
    