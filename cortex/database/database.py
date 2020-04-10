
from cortex.utils.url import parse_url

from cortex.database.database_runner import run_database

def run_database(db_url=None):
    """Starts a database to which snapshots can be saved"""  
    database_type, database_host, database_port  =   \
        parse_url(db_url)
    run_database(database_type, database_host, database_port)
    