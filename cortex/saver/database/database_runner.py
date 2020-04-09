import os 
from cortex.utils import DynamicModuleLoader 
from cortex.utils import run_bash_scipt
from cortex.utils import get_project_file_path_by_caller

import logging
from cortex.logger import _LoggerLoader

from cortex.saver.database.postgresql_db import PostgreSQLDataBase

# Log loading
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()
logger                    = logging.getLogger(__name__)

# Messages Section
# Info Messages
INSTALLING_DATABASE_INFO_MESSAGE                           =   'Installing data base...'
DATABASE_INSTALLATION_COMPLETED_INFO_MESSAGE               =   'Data base installation completed!'

# Error messages
DATABASE_TYPE_NOT_FOUND_ERROR_MESSAGE                      =   'Specified data base class not found in directory'
DATABASE_INSTALL_FILE_DOSENT_EXIST_ERROR_MESSAGE_FORMAT    =   'Data base install file {} dosen\'t exist'
DATABASE_INSTALLATION_FAILED_ERROR_MESSAGE                 =   'Data base installation has failed'

# Installation file
DATABASE_INSTALLATION_FILE_SUFFIX                          =   '_install.sh'

def load_database(database_type, host, port):
    LOOKUP_TOKEN        =   'DataBase'
    NAME_IDENTIFIER     =   'name'    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    imported_modules_names = DynamicModuleLoader.load_modules(dir_path)
    _, class_dbs = \
        DynamicModuleLoader.dynamic_lookup_to_dictionary(imported_modules_names, LOOKUP_TOKEN, NAME_IDENTIFIER)
    if database_type not in class_dbs:
        logger.error(DATABASE_TYPE_NOT_FOUND_ERROR_MESSAGE)
        return None
    # Returning specified data base object
    return class_dbs[database_type](logger, host, port)

def get_message_install_file_path(database_type):
    return get_project_file_path_by_caller(database_type, DATABASE_INSTALLATION_FILE_SUFFIX)

def install_database(database_type):
    # Installing data base
    database_install_file_path = get_message_install_file_path(database_type)    
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

def run_database(database_type  =   None,
                 host           =   None,
                 port           =   None):
    database_type  = database_type if database_type else PostgreSQLDataBase.name
    database       = load_database(database_type, host, port)
    # If data base not found - exit
    if not database:
        return
    # Else, data base found - install & run
    else:
        # If data base installed
        if install_database(database_type):
            return database.run()
    