import pika

from cortex.publisher_consumer.message_queue.message_queue import MessageQueue

# Constants definition
RABBITMQ_DEFAULT_HOST               =   '0.0.0.0'
RABBITMQ_DEFAULT_PORT               =   5672

class RabbitMQMessageQueue(MessageQueue):
    
    name            = 'rabbitmq'
    
    def _default_hostname_resolution(self, host, port):
        self.host                       = host if host else RABBITMQ_DEFAULT_HOST
        self.port                       = port if port else RABBITMQ_DEFAULT_PORT
    
    def _set_connections_parameters(self):
        self.params     = pika.ConnectionParameters(self.host, int(self.port))
    
    def _health_check(self):
        connection      = None
        try:
            self._set_connections_parameters()
            connection  = pika.BlockingConnection(self.params)
            self._logger.info(f'{RabbitMQMessageQueue.name} is available!')
            return True
        except Exception as error:
            self._logger.warning(f'{RabbitMQMessageQueue.name} at {self.host}:{self.port} not available : {error}')
            return False
        finally:
            if connection and connection.is_open:            
                connection.close()
        
    # Generates callback with custom arguments - by this currying function 
    def generate_message_callback(self):
        def callback(channel, method, properties, body):
            self.callback(body)
            channel.basic_ack(delivery_tag = method.delivery_tag)    
        return callback
    
    def _init_reciver(self):
        try:
            self._set_connections_parameters()
            self.connection = pika.BlockingConnection(self.params)
            self.channel    = self.connection.channel()
            if self.message_queue_context.exchange_name:
                self.channel.exchange_declare(self.message_queue_context.exchange_name, exchange_type=self.message_queue_context.exchange_type)
            self.channel.queue_declare(
                    queue   =   self.message_queue_context.queue_name, 
                    durable =   True
                )
            # If binding keys have been specified, binding queue to them
            if self.message_queue_context.binding_keys:
                for binding_key in self.message_queue_context.binding_keys:
                    self.channel.queue_bind(
                        exchange    =   self.message_queue_context.exchange_name, 
                        queue       =   self.message_queue_context.queue_name,
                        routing_key =   binding_key
                        )
        except Exception as ex:
            self._logger.error(ex)
        return True
    
    def _init_transmitter(self):
        try:
            self.params     = pika.ConnectionParameters(self.host)
            self.connection = pika.BlockingConnection(self.params)
            self.channel    = self.connection.channel()
            if self.message_queue_context.exchange_name:
                self.channel.exchange_declare(self.message_queue_context.exchange_name, exchange_type=self.message_queue_context.exchange_type)
        except Exception as ex:
            self._logger.error(ex.message)
            return False
        return True
   
    def _run_reciver(self):
        self.channel.basic_consume(
            queue                   =    self.message_queue_context.queue_name, 
            on_message_callback     =    self.generate_message_callback()
            )
        self.channel.start_consuming()
    
    def _messege_queue_publish(self, message, publisher_name=''):
        self.channel.basic_publish(
            exchange                =    self.message_queue_context.exchange_name, 
            routing_key             =    publisher_name, 
            body                    =    message
            )
    
    def _run_transmitter(self):
        return self._messege_queue_publish
    