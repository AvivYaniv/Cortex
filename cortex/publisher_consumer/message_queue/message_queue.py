
# Messages Section
MESSAGE_QUEUE_DIRECTION_UNSPECIFIED_ERROR_MESSAGE       =   'Message Queue direction (reciver/transmitter) unspecified!'
MESSAGE_QUEUE_HAS_NOT_INITIALIZED_ERROR_MESSAGE         =   'Message Queue has not initialized'

MESSAGE_QUEUE_INITIALIZING_INFO_MESSAGE                 =   'Message Queue initializing...'
MESSAGE_QUEUE_HAS_INITIALIZED_INFO_MESSAGE              =   'Message Queue has initialized'
        
MESSAGE_QUEUE_IS_RUNNING_INFO_MESSAGE                   =   'Message Queue ready & runs!'

# Constants Section
MESSAGE_QUEUE_DEFAULT_HOST								=	'localhost'

class MessageQueue:
    
    def _init_reciver(self):
        raise NotImplementedError
    
    def _init_transmitter(self):
        raise NotImplementedError
        
    def _init_message_queue(self):
        if self.message_queue_context.is_reciver():
            return self._init_reciver()
        elif self.message_queue_context.is_transmitter():
            return self._init_transmitter()
        else:
            self._logger.error(MESSAGE_QUEUE_DIRECTION_UNSPECIFIED_ERROR_MESSAGE)
            return False
            
    def __init__(self, logger, callback, message_queue_context, host, port):
        print(f'TODO DEUG REMOVE {host}')
        self._logger                    = logger
        self._logger.info(MESSAGE_QUEUE_INITIALIZING_INFO_MESSAGE)
        self.callback                   = callback
        self.message_queue_context      = message_queue_context
        self.host                       = host if host else MESSAGE_QUEUE_DEFAULT_HOST
        self.port                       = port
        self.is_initialized             = self._init_message_queue()
        if self.is_initialized:
            self._logger.info(MESSAGE_QUEUE_HAS_INITIALIZED_INFO_MESSAGE)
        else:
            self._logger.error(MESSAGE_QUEUE_HAS_NOT_INITIALIZED_ERROR_MESSAGE)
    
    def _run_reciver(self):
        raise NotImplementedError
    
    def _messege_queue_publish(self, message, routing_key=''):
        raise NotImplementedError
    
    def _run_transmitter(self):
        raise NotImplementedError
    
    def run(self):
        if self.is_initialized:
            if self.message_queue_context.is_reciver():
                self._run_reciver()
            elif self.message_queue_context.is_transmitter():
                return self._run_transmitter()
            