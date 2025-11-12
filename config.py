import os
from dotenv import load_dotenv

# load_dotenv()

DB_NAME = os.getenv("DB_NAME", "mqtt_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_HOST = os.getenv("DB_HOST", "192.168.1.10")
DB_PORT = os.getenv("DB_PORT", 5432)

GRPC_SERVER_ADDR = os.getenv("GRPC_SERVER_ADDR", "192.168.1.10:9090")
MQTT_BROKER = os.getenv("MQTT_BROKER", "192.168.1.10")
MQTT_PORT = os.getenv("MQTT_PORT", 1883)
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "client")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "123456")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "ESP32/cmd")