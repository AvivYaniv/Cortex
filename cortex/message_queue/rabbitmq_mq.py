import pika

# Messages
RABBIT_MQ_DIRECTION_UNSPECIFIED_ERROR_MESSAGE       =   'RabbitMQ direction (reciver/transmitter) unspecified!'
RABBIT_MQ_HAS_NOT_INITIALIZED_ERROR_MESSAGE         =   'RabbitMQ has not initialized'

RABBIT_MQ_INITIALIZING_INFO_MESSAGE                 =   'RabbitMQ initializing...'
RABBIT_MQ_HAS_INITIALIZED_INFO_MESSAGE              =   'RabbitMQ has initialized'
        
RABBIT_MQ_IS_RUNNING_INFO_MESSAGE                   =   'RabbitMQ ready & runs!'

class RabbitMQMessageQueue:
    
    name            = 'rabbitmq'
        
    # Generates callback with custom arguments - by this currying function 
    def generate_callback(self):
        def callback(channel, method, properties, body):
            self.callback(body)
            channel.basic_ack(delivery_tag = method.delivery_tag)    
        return callback
    
    def _init_reciver(self):
        try:
            self.params     = pika.ConnectionParameters(self.host)
            self.connection = pika.BlockingConnection(self.params)
            self.channel    = self.connection.channel()
            self.channel.exchange_declare(self.message_queue_context.exchange_name, exchange_type=self.message_queue_context.exchange_type)
            self.channel.queue_declare(
                    queue   =   self.message_queue_context.queue_name, 
                    durable =   True
                )
            # If no binding keys - registering to default
            if not self.message_queue_context.binding_keys:
                self.channel.queue_bind(
                    exchange    =   self.message_queue_context.exchange_name, 
                    queue       =   self.message_queue_context.queue_name
                    )
            # Else, binding keys have been specified, binding queue to them
            else:
                for binding_key in self.message_queue_context.binding_keys:
                    self.channel.queue_bind(
                        exchange    =   self.message_queue_context.exchange_name, 
                        queue       =   self.message_queue_context.queue_name,
                        routing_key =   binding_key
                        )
        except Exception as ex:
            self.logger.error(ex.message)
        return True
    
    def _init_transmitter(self):
        try:
            self.params     = pika.ConnectionParameters(self.host)
            self.connection = pika.BlockingConnection(self.params)
            self.channel    = self.connection.channel()
            self.channel.exchange_declare(self.message_queue_context.exchange_name, exchange_type=self.message_queue_context.exchange_type)
        except Exception as ex:
            self.logger.error(ex.message)
            return False
        return True
        
    def _init_rabbit_mq(self):
        if self.message_queue_context.is_reciver():
            return self._init_reciver()
        elif self.message_queue_context.is_transmitter():
            return self._init_transmitter()
        else:
            self.logger.error(RABBIT_MQ_DIRECTION_UNSPECIFIED_ERROR_MESSAGE)
            return False
            
    def __init__(self, logger, callback, message_queue_context, host='localhost'):
        self.logger = logger
        self.logger.info(RABBIT_MQ_INITIALIZING_INFO_MESSAGE)
        self.callback                   = callback
        self.message_queue_context      = message_queue_context
        self.host                       = host
        self.is_initialized             = self._init_rabbit_mq()
        if self.is_initialized:
            self.logger.info(RABBIT_MQ_HAS_INITIALIZED_INFO_MESSAGE)
        else:
            self.logger.error(RABBIT_MQ_HAS_NOT_INITIALIZED_ERROR_MESSAGE)
    
    def _run_reciver(self):
        self.channel.basic_consume(
            queue                   =    self.message_queue_context.queue_name, 
            on_message_callback     =    self.generate_callback()
            )
        self.channel.start_consuming()
    
    def _messege_queue_publish(self, message, routing_key=''):
        self.channel.basic_publish(
            exchange                =    self.message_queue_context.exchange_name, 
            routing_key             =    routing_key, 
            body                    =    message
            )
    
    def _run_transmitter(self):
        return self._messege_queue_publish
    
    def run(self):
        if self.is_initialized:
            if self.message_queue_context.is_reciver():
                self._run_reciver()
            elif self.message_queue_context.is_transmitter():
                return self._run_transmitter()
            