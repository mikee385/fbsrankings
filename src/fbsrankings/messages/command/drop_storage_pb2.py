# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: fbsrankings/messages/command/drop_storage.proto
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
    'fbsrankings/messages/command/drop_storage.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fbsrankings.messages.options import options_pb2 as fbsrankings_dot_messages_dot_options_dot_options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/fbsrankings/messages/command/drop_storage.proto\x12\x1c\x66\x62srankings.messages.command\x1a*fbsrankings/messages/options/options.proto\"N\n\x12\x44ropStorageCommand\x12\x12\n\ncommand_id\x18\x01 \x01(\t:$\x82\xb5\x18 fbsrankings.command.drop_storageb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fbsrankings.messages.command.drop_storage_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DROPSTORAGECOMMAND']._loaded_options = None
  _globals['_DROPSTORAGECOMMAND']._serialized_options = b'\202\265\030 fbsrankings.command.drop_storage'
  _globals['_DROPSTORAGECOMMAND']._serialized_start=125
  _globals['_DROPSTORAGECOMMAND']._serialized_end=203
# @@protoc_insertion_point(module_scope)
