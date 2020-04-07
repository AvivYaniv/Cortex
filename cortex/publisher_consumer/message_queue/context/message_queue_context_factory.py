
from cortex.utils.dictionary_to_object import dictionary_to_object

from cortex.publisher_consumer.message_queue.rabbitmq_mq import RabbitMQMessageQueue
from cortex.publisher_consumer.message_queue.context.message_queue_context import MessageQueueContext
from cortex.publisher_consumer.message_queue.context.message_queue_context_loader import _MessageQueueContextLoader

import ast

import  logging
from    cortex.logger import _LoggerLoader

# Log initialization
logger                    = logging.getLogger(__name__)
logger_loader             = _LoggerLoader()
logger_loader.load_log_config()

# Constants Section
RESERVED_KEYWORDS_FORMAT                =   '<%s>'
MESSAGE_QUEUE_DICTIONAY_HEADER          =   'message_queue'

RECIVERS_CATEGORIES_NAMES               =   [ 'consumers' ]
TRANSMITTERS_CATEGORIES_NAMES           =   [ 'publishers' ]

class MessageQueueContextFactory:
    def __init__(self, message_queue_type = None):
        message_queue_type              =   message_queue_type if message_queue_type else RabbitMQMessageQueue.name
        # Invoking the message queue context loader configuration loader
        message_queue_context_loader    =   _MessageQueueContextLoader(message_queue_type)
        # Setting message queue loaded context dictionary
        self.config_dictionary          =   message_queue_context_loader.get_mq_config()

    # Returns category dictionary
    def _get_category_dictionary(self, caller_type, category):
        dict_message_queue      =   self.config_dictionary[MESSAGE_QUEUE_DICTIONAY_HEADER]
        dict_type               =   dict_message_queue[caller_type]
        dict_category           =   dict_type[category]
        return dict_category
    
    def _get_category_item_names(self, caller_type, category):
        dict_category = self._get_category_dictionary(caller_type, category)
        items = []
        for c in dict_category:
            items += list(c.keys())
        return items
    
    # Returns category contexts raw
    def _get_mq_category_dictionaries_raw(self, caller_type, category):
        dict_category = self._get_category_dictionary(caller_type, category)
        category_items = []
        for c in dict_category:
            category_items += list(c.values())
        return category_items
    
    # Returns the relevant part from the context dictionary that describes how to build current context
    def _get_mq_context_raw(self, caller_type, category, item):
        dict_category = self._get_category_dictionary(caller_type, category)
        for c in dict_category:
            if item in c:
                dict_item       =   c[item]
        return dict_item
    
    @staticmethod
    def replace_reserved_keywords(s, **kwargs):
        for key, value in kwargs.items():
            s = s.replace(RESERVED_KEYWORDS_FORMAT % key, value)            
        return s
    
    @staticmethod
    def _convert_raw_dict_to_context(raw_context_dict, category, **kwargs):
        raw_dict_as_str             = str(raw_context_dict)
        raw_dict_replaced_as_str    = \
            MessageQueueContextFactory.replace_reserved_keywords(raw_dict_as_str, **kwargs)
        raw_dict_replaced           = ast.literal_eval(raw_dict_replaced_as_str)
        message_queue_context       = dictionary_to_object(raw_dict_replaced, MessageQueueContext)
        MessageQueueContextFactory.set_message_queue_role(message_queue_context, category)
        return message_queue_context
    
    @staticmethod
    def set_message_queue_role(message_queue_context, category):
        if category in RECIVERS_CATEGORIES_NAMES:
            message_queue_context.set_reciver()
        elif category in TRANSMITTERS_CATEGORIES_NAMES:
            message_queue_context.set_transmitter()
       
    def get_mq_category_contexts(self, caller_type, category, **kwargs):
        message_queue_category_contexts     =   []
        raw_category_dctionaries            =   \
            self._get_mq_category_dictionaries_raw(caller_type, category)
        for raw_context_dict in raw_category_dctionaries:
            message_queue_context   =                                       \
                MessageQueueContextFactory._convert_raw_dict_to_context(    \
                raw_context_dict,                                           \
                category,                                                   \
                **kwargs)  
            message_queue_category_contexts.append(message_queue_context)
        return message_queue_category_contexts
            
    def get_mq_context(self, caller_type, category, item, **kwargs):
        raw_context_dict        =   self._get_mq_context_raw(caller_type, category, item)
        message_queue_context   =   MessageQueueContextFactory._convert_raw_dict_to_context(raw_context_dict, category, **kwargs)
        return message_queue_context

