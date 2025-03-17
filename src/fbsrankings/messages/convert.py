from datetime import date
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp


def datetime_to_timestamp(value: datetime) -> Timestamp:
    timestamp = Timestamp()
    timestamp.FromDatetime(value)
    return timestamp


def date_to_timestamp(value: date) -> Timestamp:
    return datetime_to_timestamp(datetime.combine(value, datetime.min.time()))
