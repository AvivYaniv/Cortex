from cortex.database.database_runner import run_database

from cortex.envvars import get_database_parameters

def run_database_container():
    database_type, database_host, database_port = get_database_parameters()
    run_database(database_type, database_host, database_port)

if "__main__" == __name__:
    run_database_container()
    