import pika

# Messages
RABBIT_MQ_INITIALIZING_INFO_MESSAGE =   'RabbitMQ initializing...'

# Commands
START_RABBIT_MQ_SERVER_COMMAND      =   'sudo services start rabbitmq'

class RabbitMQMessageQueue:
    
    name = 'rabbitmq'
    
    def _init_rabbit_mq(self, host):
        self.params     = pika.ConnectionParameters(host)
        self.connection = pika.BlockingConnection(self.params)
        self.channel    = self.connection.channel()
    
    def __init__(self, logger, host='localhost'):
        self.logger = logger
        self.logger.info(RABBIT_MQ_INITIALIZING_INFO_MESSAGE)
        self._init_rabbit_mq(host)
        
    def run(self):
        # TODO implement
        print("I believe I can run")
        pass