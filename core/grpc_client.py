import grpc
import asyncio
from gen import ble_pb2, ble_pb2_grpc

GRPC_SERVER_ADDR = "192.168.1.61:9090"

async def scan_ble():
    """Gọi hàm Scan() (server-streaming RPC)"""
    loop = asyncio.get_running_loop()

    def blocking_scan():
        devices = []
        with grpc.insecure_channel(GRPC_SERVER_ADDR) as channel:
            stub = ble_pb2_grpc.BLEServiceStub(channel)
            for event in stub.Scan(ble_pb2.ScanRequest(duration_seconds=5)):
                if event.message:
                    print("[log]", event.message)
                else:
                    devices.append({
                        "name": event.name,
                        "mac": event.mac,
                        "rssi": event.rssi,
                    })
        return devices

    return await loop.run_in_executor(None, blocking_scan)

async def connect_ble(mac: str):
    """Gọi hàm Connect() (unary RPC)"""
    loop = asyncio.get_running_loop()

    def blocking_connect():
        with grpc.insecure_channel(GRPC_SERVER_ADDR) as channel:
            stub = ble_pb2_grpc.BLEServiceStub(channel)
            response = stub.Connect(ble_pb2.ConnectRequest(mac=mac, ssid="Phong 9", password="12312312", mqtt="192.168.1.61"))
            return response

    return await loop.run_in_executor(None, blocking_connect)