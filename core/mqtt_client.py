import paho.mqtt.client as mqtt
import time
import config

BROKER = config.MQTT_BROKER
PORT = config.MQTT_PORT
TOPIC = config.MQTT_TOPIC
USERNAME = config.MQTT_USERNAME
PASSWORD = config.MQTT_PASSWORD

def on_publish(client, userdata, mid):
    print(f"📤 Message published (mid={mid})")

def create_mqtt_client():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_publish = on_publish
    client.connect(BROKER, PORT, 60)
    return client

def publish_message(topic: str, message: str):
    client = create_mqtt_client()
    client.loop_start()
    while not client.is_connected():
        time.sleep(0.1)
    result = client.publish(topic, message)
    status = result[0]
    client.loop_stop()
    client.disconnect()
    return status == 0


def publish_message_cmd(sensor: str, message: str):
    return publish_message(f"{sensor}/cmd", message)