#!/usr/bin/env python

import argparse

from constants import TOPIC
from mqtt_connection import MqttConnection
from utils import setup_logging, waitForKeyboardInterrupt


def on_connect(mqtt_client, userdata, flags, rc):
    print("Connected with result code: {0}".format(rc))
    mqtt_client.subscribe(userdata[TOPIC])


def on_subscribe(mqtt_client, userdata, mid, granted_qos):
    print("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


def on_message(mqtt_client, userdata, msg):
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    print("{0} : {1}".format(msg.topic, val))
    # If payload is an int byte array, use: int.from_bytes(msg.payload, byteorder="big"))
    # int.from_bytes() requires python3: https://docs.python.org/3/library/stdtypes.html#int.from_bytes


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    parser.add_argument("-t", "--topic", required=True, help="MQTT topic")
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging()

    # Setup MQTT client
    with MqttConnection(args["mqtt"],
                        userdata={TOPIC: args["topic"]},
                        on_connect=on_connect,
                        on_subscribe=on_subscribe,
                        on_message=on_message):
        waitForKeyboardInterrupt()

    print("Exiting...")
