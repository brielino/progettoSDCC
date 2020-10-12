import json

import paho.mqtt.client as mqtt #import the client1
import time
############
broker_address="18.224.107.213"
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
#broker_address="localhost"
#broker_address="test.mosquitto.org"

def sendData(data):
    print("creating new instance")
    client = mqtt.Client("P1") #create new instance
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    print("Subscribing to topic", "house/bulbs/bulb1")
    print("Publishing message to topic", json.dumps(data))
    client.publish("pazienti/sensori", json.dumps(data))
    time.sleep(1) # wait
    client.loop_stop() #stop the loop
