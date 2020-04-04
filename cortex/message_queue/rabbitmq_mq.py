import pika
from builtins import staticmethod

# Messages
RABBIT_MQ_INITIALIZING_INFO_MESSAGE     =   'RabbitMQ initializing...'
RABBIT_MQ_HAS_INITIALIZED_INFO_MESSAGE  =   'RabbitMQ has initialized'

RABBIT_MQ_IS_RUNNING_INFO_MESSAGE       =   'RabbitMQ ready & runs!'

class RabbitMQMessageQueue:
    
    name            = 'rabbitmq'
    
    queue_name      = 'message_queue'
    
    @staticmethod
    def callback(channel, method, properties, body):
        print(body)
    
    def _init_rabbit_mq(self, host):
        self.params     = pika.ConnectionParameters(host)
        self.connection = pika.BlockingConnection(self.params)
        self.channel    = self.connection.channel()
        self.channel.queue_declare(
                queue   =   RabbitMQMessageQueue.queue_name, 
                durable =   True, 
            )
    
    def __init__(self, logger, host='localhost'):
        self.logger = logger
        self.logger.info(RABBIT_MQ_INITIALIZING_INFO_MESSAGE)
        self._init_rabbit_mq(host)
        self.logger.info(RABBIT_MQ_HAS_INITIALIZED_INFO_MESSAGE)
        
    def run(self):
        self.logger.info(RABBIT_MQ_IS_RUNNING_INFO_MESSAGE)
        self.channel.basic_consume(
                queue                   =   RabbitMQMessageQueue.queue_name, 
                on_message_callback     =   RabbitMQMessageQueue.callback
            )
            