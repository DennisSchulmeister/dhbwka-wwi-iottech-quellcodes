from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import json
from mqtt.subsciber import init_mqtt, listen_subsciptions
from mongo.data_sink import get_connection, insert_document
from mongo.collection_name_generator import derive_collection_name

mqtt_client = init_mqtt()

sensor_db = get_connection()


def callback(client, userdata, msg):
    print(f"Incoming data from {msg.topic} : {msg.payload}")
    decoded = json.loads(msg.payload.decode("utf-8"))
    insert_document(
        client=sensor_db,
        collection_name=derive_collection_name(msg.topic),
        data_list=decoded.get("values")
    )


mqtt_client.on_message = callback

listen_subsciptions(mqtt_client)
