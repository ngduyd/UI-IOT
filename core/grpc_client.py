import grpc
import asyncio
from gen import ble_pb2, ble_pb2_grpc, wifi_pb2, wifi_pb2_grpc
import os, json
import config

CONFIG_PATH = 'config.json'

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"mode": "Wi-Fi", "ssid": "", "password": "", "mqtt": "", "isConfigured": False, "usingmDNS": False}

GRPC_SERVER_ADDR = config.GRPC_SERVER_ADDR

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
            config = load_config()
            response = stub.Connect(ble_pb2.ConnectRequest(mac=mac, ssid=config.get("ssid", ""), password=config.get("password", ""), mqtt=config.get("mqtt", "")))
            return response

    return await loop.run_in_executor(None, blocking_connect)

async def test_wifi_connection(ssid: str, password: str):
    """Gọi hàm TestConnection() (unary RPC)"""
    loop = asyncio.get_running_loop()

    def blocking_test():
        with grpc.insecure_channel(GRPC_SERVER_ADDR) as channel:
            stub = wifi_pb2_grpc.WifiServiceStub(channel)
            response = stub.TestConnection(wifi_pb2.TestRequest(ssid=ssid, password=password, timeout_seconds=10))
            return response

    return await loop.run_in_executor(None, blocking_test)

async def connect_wifi(ssid: str, password: str):
    """Gọi hàm Connect() (unary RPC)"""
    loop = asyncio.get_running_loop()

    def blocking_connect():
        with grpc.insecure_channel(GRPC_SERVER_ADDR) as channel:
            stub = wifi_pb2_grpc.WifiServiceStub(channel)
            response = stub.Connect(wifi_pb2.WifiCredentials(ssid=ssid, password=password))
            return response

    return await loop.run_in_executor(None, blocking_connect)