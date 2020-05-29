
from cortex.utils.url import parse_url

from cortex.saver.saver_service import SaverService
from cortex.saver.saver_service import run_saver_service

from cortex.utils import _FileHandler

class Saver:
    def __init__(self, db_url=None):
        database_type, database_host, database_port  =   \
        parse_url(db_url)
        self.saver_service = SaverService(database_type, database_host, database_port)
    
    def get_database(self):
        return self.saver_service.saver_messges_handler._database
    
    def save_message(self, message_data):
        return self.saver_service.handle_message(message_data)
    
    def save(self, message_path):
        result, message = _FileHandler.safe_read_file(message_path)
        if not result:
            return message
        return self.save_message(message)

def save(message):
    saver = Saver()
    return saver.save(message)

def run_saver(db_url=None, mq_url=None):
    """Starts a saver to which snapshots can be uploaded with `upload_sample`"""  
    database_type, database_host, database_port  =   \
        parse_url(db_url)
    message_queue_type, message_queue_host, message_queue_port  =   \
        parse_url(mq_url)
    saver_service = run_saver_service(database_type, database_host, database_port, message_queue_type, message_queue_host, message_queue_port)
    saver_service.run()
