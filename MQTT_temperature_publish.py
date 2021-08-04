#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import Adafruit_DHT
import time
import json

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def on_connect(client, userdata, flags,rc):
    global loop_flag
    loop_flag = 0

def on_publsh(client, userdata, result):
    print("Data published \n")
    pass

broker_address = "localhost"
client = mqtt.Client()
client.on_connect=on_connect
client.connect(broker_address)
client.loop_start()

loop_flag=1
counter=0
while loop_flag==1:
    print("Waiting for callback ",counter)
    counter+=1
    time.sleep(.01)




while True:
    print("connecting to sensor")
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        msg = json.dumps({"temperature": {"temp": temperature,"humidity": humidity,"tempScale": "celcius"}})
        ret = client.publish("Dutzo",msg)
    else:
        print("Failed to retrieve data from humidity sensor")
    time.sleep(10)
