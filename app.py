from concurrent import futures

import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

import kvstore_pb2_grpc
from servicer import KeyValueStoreServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStoreServicer(), server
    )

    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)

    server.add_insecure_port("0.0.0.0:8000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
