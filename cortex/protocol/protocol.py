from cortex.protocol.native import *
from cortex.protocol.protobuf import *

class ProtocolMessagesTyeps:
    HELLO_MESSAGE       = 0
    CONFIG_MESSAGE      = 1
    SNAPSHOT_MESSAGE    = 2

class ProtocolTypes:
    NATIVE_PROTOCOL     = 0
    PROTOBUF_PROTOCOL   = 1

class Protocol:
    NATIVE_MESSAGES =                                                           \
        {                                                                       \
            ProtocolMessagesTyeps.HELLO_MESSAGE     : HelloMessageNative,       \
            ProtocolMessagesTyeps.CONFIG_MESSAGE    : ConfigMessageNative,      \
            ProtocolMessagesTyeps.SNAPSHOT_MESSAGE  : SnapshotMessageNative,    \
        }
    
    PROTOBUF_MESSAGES =                                                         \
        {                                                                       \
            ProtocolMessagesTyeps.HELLO_MESSAGE     : HelloMessageProto,        \
            ProtocolMessagesTyeps.CONFIG_MESSAGE    : ConfigMessageProto,       \
            ProtocolMessagesTyeps.SNAPSHOT_MESSAGE  : SnapshotMessageProto,     \
        }
    
    PROTOCOLS_MESSAGES_TABLE =                                                  \
        {                                                                       \
            ProtocolTypes.NATIVE_PROTOCOL   : NATIVE_MESSAGES,                  \
            ProtocolTypes.PROTOBUF_PROTOCOL : PROTOBUF_MESSAGES,                \
        }
    
    def __init__(self, protocol_type=ProtocolTypes.PROTOBUF_PROTOCOL):
        self.protocol_messages = Protocol.PROTOCOLS_MESSAGES_TABLE[protocol_type]
        
    def get_message(self, message_type):
        return self.protocol_messages[message_type]
        