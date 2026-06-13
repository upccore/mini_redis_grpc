from grpclib import GRPCError, Status
from grpclib.server import Stream

import kvstore_pb2
from kvstore_grpc import KeyValueStoreBase
from store import KVStore


class KeyValueStoreService(KeyValueStoreBase):
    def __init__(self):
        self._store = KVStore()

    async def Put(
        self, stream: Stream[kvstore_pb2.PutRequest, kvstore_pb2.PutResponse]
    ) -> None:
        request = await stream.recv_message()
        self._store.put(request.key, request.value, request.ttl_seconds)
        await stream.send_message(kvstore_pb2.PutResponse())

    async def Get(
        self, stream: Stream[kvstore_pb2.GetRequest, kvstore_pb2.GetResponse]
    ) -> None:
        request = await stream.recv_message()
        value = self._store.get(request.key)
        if value is None:
            raise GRPCError(Status.NOT_FOUND, f"key '{request.key}' not found")
        await stream.send_message(kvstore_pb2.GetResponse(value=value))

    async def Delete(
        self, stream: Stream[kvstore_pb2.DeleteRequest, kvstore_pb2.DeleteResponse]
    ) -> None:
        request = await stream.recv_message()
        self._store.delete(request.key)
        await stream.send_message(kvstore_pb2.DeleteResponse())

    async def List(
        self, stream: Stream[kvstore_pb2.ListRequest, kvstore_pb2.ListResponse]
    ) -> None:
        request = await stream.recv_message()
        items = self._store.list_prefix(request.prefix)
        await stream.send_message(
            kvstore_pb2.ListResponse(
                items=[kvstore_pb2.KeyValue(key=k, value=v) for k, v in items]
            )
        )
