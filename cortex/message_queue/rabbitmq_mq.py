class RabbitMQMessageQueue:
    
    name = 'rabbitmq'
    
    def __init__(self, logger):
        print('Sabich all the time!!!')
        self.logger = logger
        self.logger.info("MQ SUCCESS!")
        
    def run(self):
        # TODO implement
        print("I believe I can run")
        pass