import io

from cortex.protobuf import protocol_proto

from cortex.protocol.config_message import ConfigMessage

from cortex.utils import Serialization

class ConfigMessageProto(ConfigMessage):
    
    def serialize(self):
        config_message          = protocol_proto.ConfigMessage()
        for field in self.fields:
            proto_field 		= config_message.fields_config.fields.add()
            proto_field.name 	= field            
        return Serialization.serialize_tunnled_message(config_message.SerializeToString())
    
    @staticmethod
    def read(data):
        stream = io.BytesIO(data)
        return ConfigMessageProto.read_stream(stream)
    
    @staticmethod
    def read_stream(stream):
        config_message_bytes         =  Serialization.read_tunnled_message(stream)
        config_message_protobuf      =  protocol_proto.ConfigMessage()
        config_message_protobuf.ParseFromString(config_message_bytes)
        fields_config                =  [f.name for f in config_message_protobuf.fields_config.fields]
        config_message               =  ConfigMessage(fields_config)
        return config_message
        