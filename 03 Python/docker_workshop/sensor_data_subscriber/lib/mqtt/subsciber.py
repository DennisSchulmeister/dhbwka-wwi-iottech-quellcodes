from os import getenv
from paho.mqtt.client import Client
from threading import Thread

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(getenv('MQTT_BROKER_TOPIC'))

def init_mqtt() -> Client:
    host = getenv('MQTT_BROKER_HOST')
    port = getenv('MQTT_BROKER_PORT')
    if host is None or port is None:
        raise ValueError(f'host: {host} , port: {port} combination not valid!')
    client = Client(client_id=getenv('MQTT_CLIENT_ID'))
    client.on_connect = on_connect
    client.connect(host, int(port), 60)
    return client


def listen_subsciptions(client: Client):
    clientloop_thread = Thread(target=lambda: client.loop_forever())
    clientloop_thread.start()