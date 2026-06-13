import os
from concurrent import futures

import grpc

import kvstore_pb2_grpc
from servicer import KeyValueStoreServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(), server
    )

    port = int(os.environ.get("PORT", "8000"))
    server.add_insecure_port(f"0.0.0.0:{port}")
    server.add_insecure_port("0.0.0.0:50051")

    server.start()
    print(f"gRPC server listening on port {port} and 50051", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
