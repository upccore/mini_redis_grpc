import grpc

import kvstore_pb2
import kvstore_pb2_grpc
from store import KVStore


class KeyValueStoreServicer(kvstore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self._store = KVStore()

    def Put(self, request, context):
        self._store.put(request.key, request.value, request.ttl_seconds)
        return kvstore_pb2.PutResponse()

    def Get(self, request, context):
        value = self._store.get(request.key)
        if value is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"key '{request.key}' not found")
        return kvstore_pb2.GetResponse(value=value)

    def Delete(self, request, context):
        self._store.delete(request.key)
        return kvstore_pb2.DeleteResponse()

    def List(self, request, context):
        items = self._store.list_prefix(request.prefix)
        return kvstore_pb2.ListResponse(
            items=[kvstore_pb2.KeyValue(key=k, value=v) for k, v in items]
        )
