# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fbsrankings/messages/query/team_record_by_season_week.proto
# Protobuf Python Version: 6.30.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    30,
    1,
    '',
    'fbsrankings/messages/query/team_record_by_season_week.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fbsrankings.messages.options import options_pb2 as fbsrankings_dot_messages_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n;fbsrankings/messages/query/team_record_by_season_week.proto\x12\x1a\x66\x62srankings.messages.query\x1a*fbsrankings/messages/options/options.proto\"`\n!TeamRecordValueBySeasonWeekResult\x12\x0f\n\x07team_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04wins\x18\x03 \x01(\x05\x12\x0e\n\x06losses\x18\x04 \x01(\x05\"\xbc\x01\n\x1bTeamRecordBySeasonWeekValue\x12\x11\n\trecord_id\x18\x01 \x01(\t\x12\x11\n\tseason_id\x18\x02 \x01(\t\x12\x0c\n\x04year\x18\x03 \x01(\x05\x12\x11\n\x04week\x18\x04 \x01(\x05H\x00\x88\x01\x01\x12M\n\x06values\x18\x05 \x03(\x0b\x32=.fbsrankings.messages.query.TeamRecordValueBySeasonWeekResultB\x07\n\x05_week\"\x89\x01\n\x1cTeamRecordBySeasonWeekResult\x12\x10\n\x08query_id\x18\x01 \x01(\t\x12L\n\x06record\x18\x02 \x01(\x0b\x32\x37.fbsrankings.messages.query.TeamRecordBySeasonWeekValueH\x00\x88\x01\x01\x42\t\n\x07_record\"\x90\x01\n\x1bTeamRecordBySeasonWeekQuery\x12\x10\n\x08query_id\x18\x01 \x01(\t\x12\x11\n\tseason_id\x18\x02 \x01(\t\x12\x11\n\x04week\x18\x03 \x01(\x05H\x00\x88\x01\x01:0\x82\xb5\x18,fbsrankings.query.team_record_by_season_weekB\x07\n\x05_weekb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fbsrankings.messages.query.team_record_by_season_week_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TEAMRECORDBYSEASONWEEKQUERY']._loaded_options = None
  _globals['_TEAMRECORDBYSEASONWEEKQUERY']._serialized_options = b'\202\265\030,fbsrankings.query.team_record_by_season_week'
  _globals['_TEAMRECORDVALUEBYSEASONWEEKRESULT']._serialized_start=135
  _globals['_TEAMRECORDVALUEBYSEASONWEEKRESULT']._serialized_end=231
  _globals['_TEAMRECORDBYSEASONWEEKVALUE']._serialized_start=234
  _globals['_TEAMRECORDBYSEASONWEEKVALUE']._serialized_end=422
  _globals['_TEAMRECORDBYSEASONWEEKRESULT']._serialized_start=425
  _globals['_TEAMRECORDBYSEASONWEEKRESULT']._serialized_end=562
  _globals['_TEAMRECORDBYSEASONWEEKQUERY']._serialized_start=565
  _globals['_TEAMRECORDBYSEASONWEEKQUERY']._serialized_end=709
# @@protoc_insertion_point(module_scope)
