
import random
import string

import unittest.mock

import cortex.saver.saver_service  

from cortex.saver import run_saver_service

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join([random.choice(letters) for i in range(stringLength)])

class SaverSnifferHandler:
    DEFAULT_ENCODING            =   'utf-8'    
    def __init__(self, database_type=None, database_host=None, database_port=None):
        pass
    def handle(self, message):
        message                 = message if isinstance(message, str) else message.decode(SaverSnifferHandler.DEFAULT_ENCODING)
        with open(randomString(), 'w') as f:
            f.write(message)

def patch_saver_handler():
    cortex.saver.saver_service.saver_messages_handler.SaverMessagesHandler = SaverSnifferHandler
    
if "__main__" == __name__:
    patch_saver_handler()
    run_saver_service()
    