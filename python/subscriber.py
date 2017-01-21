#!/usr/bin/env python3

import argparse
import logging
import socket

import paho.mqtt.client as paho

from utils import LOGGING_ARGS
from utils import TOPIC
from utils import mqtt_broker_info


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {0}".format(rc))
    client.subscribe(userdata[TOPIC])


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


def on_message(client, userdata, msg):
    print("{0} : {1}".format(msg.topic, int.from_bytes(msg.payload, byteorder="big")))
    # If i is a string, use: bytes.decode(msg.payload):


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    parser.add_argument("-t", "--topic", required=True, help="MQTT topic")
    args = vars(parser.parse_args())

    # Setup logging
    logging.basicConfig(**LOGGING_ARGS)

    # Create userdata dictionary
    userdata = {TOPIC: args["topic"]}

    # Initialize MQTT client
    client = paho.Client(userdata=userdata)

    # Setup MQTT callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Determine MQTT broker details
    mqtt_hostname, mqtt_port = mqtt_broker_info(args["mqtt"])

    try:
        # Connect to MQTT broker
        logging.info("Connecting to MQTT broker {0}:{1}...".format(mqtt_hostname, mqtt_port))
        client.connect(mqtt_hostname, port=mqtt_port, keepalive=60)
        client.loop_forever()
    except socket.error:
        logging.error("Cannot connect to MQTT broker {0}:{1}".format(mqtt_hostname, mqtt_port))
    except KeyboardInterrupt:
        pass

    print("Exiting...")
