# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fbsrankings/messages/command/calculate_rankings_for_season.proto
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
    'fbsrankings/messages/command/calculate_rankings_for_season.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fbsrankings.messages.options import options_pb2 as fbsrankings_dot_messages_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n@fbsrankings/messages/command/calculate_rankings_for_season.proto\x12\x1c\x66\x62srankings.messages.command\x1a*fbsrankings/messages/options/options.proto\"\xa8\x01\n!CalculateRankingsForSeasonCommand\x12\x12\n\ncommand_id\x18\x01 \x01(\t\x12\x13\n\tseason_id\x18\x02 \x01(\tH\x00\x12\x0e\n\x04year\x18\x03 \x01(\x05H\x00:5\x82\xb5\x18\x31\x66\x62srankings.command.calculate_rankings_for_seasonB\x13\n\x11season_id_or_yearb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fbsrankings.messages.command.calculate_rankings_for_season_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CALCULATERANKINGSFORSEASONCOMMAND']._loaded_options = None
  _globals['_CALCULATERANKINGSFORSEASONCOMMAND']._serialized_options = b'\202\265\0301fbsrankings.command.calculate_rankings_for_season'
  _globals['_CALCULATERANKINGSFORSEASONCOMMAND']._serialized_start=143
  _globals['_CALCULATERANKINGSFORSEASONCOMMAND']._serialized_end=311
# @@protoc_insertion_point(module_scope)
