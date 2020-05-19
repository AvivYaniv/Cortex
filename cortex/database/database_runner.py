import os 
from cortex.utils import DynamicModuleLoader 
from cortex.utils import run_bash_scipt
from cortex.utils import get_project_file_path_by_caller

import logging
from cortex.logger import _LoggerLoader

from cortex.database.mongodb_db import MongoDBDataBase

# Log loading
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()
logger                    = logging.getLogger(__name__)

# Constants Section
DEFAULT_DB                                                 =    MongoDBDataBase.name

# Messages Section
# Info Messages
# Install Info Messages
INSTALLING_DATABASE_INFO_MESSAGE                           =   'Installing data base...'
DATABASE_INSTALLATION_COMPLETED_INFO_MESSAGE               =   'Data base installation completed!'

# Shutdown Info Messages
SHUTTING_DOOWN_SATABASE_DATABASE_INFO_MESSAGE              =   'Shutting-down data base...'
DATABASE_SHUTDOWN_COMPLETED_INFO_MESSAGE                   =   'Data base shutdown completed!'

# Running Info Messages
RUNNING_DATABASE_INFO_MESSAGE                              =   'Running data base...'

# Error Messages
DATABASE_TYPE_NOT_FOUND_ERROR_MESSAGE                      =   'Specified data base class not found in directory'
# Install Error Messages
DATABASE_INSTALL_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT    =   'Data base install file {} dosen\'t exist'
DATABASE_INSTALLATION_FAILED_ERROR_MESSAGE                 =   'Data base installation has failed'
# Shutdown Error Messages
DATABASE_SHUTDOWN_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT   =   'Data base shutdown file {} dosen\'t exist'
DATABASE_SHUTDOWN_FAILED_ERROR_MESSAGE                     =   'Data base shutdown has failed'
# Run Error Messages
DATABASE_RUNN_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT       =   'Data base run file {} dosen\'t exist'
DATABASE_RUNNING_FAILED_ERROR_MESSAGE                      =   'Data base runnning has failed'

# Files suffixes
DATABASE_INSTALLATION_FILE_SUFFIX                          =   '_install.sh'
DATABASE_SHUTDOWNON_FILE_SUFFIX                            =   '_shutdown.sh'
DATABASE_RUN_FILE_SUFFIX                                   =   '_run.sh'

# Constants Section
# Networking
DEFAULT_DB_HOST            =    '0.0.0.0'
DEFAULT_DB_PORT            =    '27017'
    
# DataBase
DEFAULT_DB_TYPE            =    MongoDBDataBase.name

def load_database(database_type=None, host=None, port=None):
    LOOKUP_TOKEN        =   'DataBase'
    NAME_IDENTIFIER     =   'name'   
    # Default argument resolution 
    database_type       = database_type if database_type else DEFAULT_DB_TYPE 
    host                = host if host else DEFAULT_DB_HOST
    port                = int(port if port else DEFAULT_DB_PORT)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
    _, class_dbs = \
        DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, LOOKUP_TOKEN, NAME_IDENTIFIER)
    if database_type not in class_dbs:
        logger.error(DATABASE_TYPE_NOT_FOUND_ERROR_MESSAGE)
        return None
    # Returning specified data base object
    return class_dbs[database_type](logger, host, port)

def get_database_install_file_path(database_type):
    return get_project_file_path_by_caller(database_type, DATABASE_INSTALLATION_FILE_SUFFIX)

def get_database_run_file_path(database_type):
    return get_project_file_path_by_caller(database_type, DATABASE_RUN_FILE_SUFFIX)

def install_database(database_type):
    # Installing data base
    database_install_file_path = get_database_install_file_path(database_type)    
    # If data base install file dosen't exist
    if (not os.path.isfile(database_install_file_path)):
        logger.error(DATABASE_INSTALL_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT.format(database_install_file_path))
        return False    
    # Installing data base
    logger.info(INSTALLING_DATABASE_INFO_MESSAGE)
    intallation_success = (0 == run_bash_scipt(database_install_file_path)) 
    if intallation_success:
        logger.info(DATABASE_INSTALLATION_COMPLETED_INFO_MESSAGE)
    else:
        logger.error(DATABASE_INSTALLATION_FAILED_ERROR_MESSAGE)
    return intallation_success

def get_database_shutdown_file_path(database_type):
    return get_project_file_path_by_caller(database_type, DATABASE_SHUTDOWNON_FILE_SUFFIX)

def stop_database(database_type=None):
    database_type = database_type if database_type else DEFAULT_DB_TYPE
    # Shutting-down data base
    database_shutdown_file_path = get_database_shutdown_file_path(database_type)    
    # If data base shutdown file dosen't exist
    if (not os.path.isfile(database_shutdown_file_path)):
        logger.error(DATABASE_SHUTDOWN_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT.format(database_shutdown_file_path))
        return False    
    # Shutting-down data base
    logger.info(SHUTTING_DOOWN_SATABASE_DATABASE_INFO_MESSAGE)
    shutdown_success = (0 == run_bash_scipt(database_shutdown_file_path)) 
    if shutdown_success:
        logger.info(DATABASE_SHUTDOWN_COMPLETED_INFO_MESSAGE)
    else:
        logger.error(DATABASE_SHUTDOWN_FAILED_ERROR_MESSAGE)
    return shutdown_success

def run_database_service(database_type):
    # Running data base
    database_run_file_path = get_database_run_file_path(database_type)    
    # If data base run file dosen't exist
    if (not os.path.isfile(database_run_file_path)):
        logger.error(DATABASE_RUNN_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT.format(database_run_file_path))
        return False    
    # Running data base
    logger.info(RUNNING_DATABASE_INFO_MESSAGE)
    running_success = (0 == run_bash_scipt(database_run_file_path)) 
    if not running_success:
        logger.error(DATABASE_RUNNING_FAILED_ERROR_MESSAGE)
    return running_success

def run_database(database_type  =   None,
                 host           =   None,
                 port           =   None):
    database_type  = database_type if database_type else DEFAULT_DB_TYPE
    database       = load_database(database_type, host, port)
    # If data base not found - exit
    if not database:
        return
    # Else, data base found - install & run
    else:
        # If data base installed
        if install_database(database_type):
            run_database_service(database_type)
    