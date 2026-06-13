import asyncio
import os

from grpclib.server import Server

from servicer import KeyValueStoreService


async def main():
    port = int(os.environ.get("PORT", "8000"))
    server = Server([KeyValueStoreService()])
    await server.start("0.0.0.0", port)
    print(f"gRPC server started on port {port}", flush=True)
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
