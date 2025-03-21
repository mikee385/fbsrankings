"""Common message options that can be utilized in any package"""

from google.protobuf.message import Message

from .options_pb2 import topic


def get_topic(message_type: type[Message]) -> str:
    options = message_type.DESCRIPTOR.GetOptions()
    if not options.HasExtension(topic):
        raise ValueError(f"{message_type} does not have a 'topic' defined")
    return options.Extensions[topic]


__all__ = [
    "get_topic",
    "topic",
]
