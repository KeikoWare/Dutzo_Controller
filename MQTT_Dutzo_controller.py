#!/usr/bin/env python3
import time
import board
import neopixel
import paho.mqtt.client as mqtt
import json

# Define Variables
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 1
MQTT_TOPIC = "Dutzo"
MQTT_MSG="no shit"
CurTemp = 0
CurMode = "temperature"
CurColor = (255,0,0)

#Define function for shutting RGB pixels off 
def pixelsOff():
    global CurColor
    CurColor = (0,0,0)
    pixels.fill(CurColor)
    pixels.show()

# Define color table for temperature scale -10 <-> 100 degree celcius
def fncTemperatureColor(temperature):
    baseTemp = 20.0 # Base temperature (green'ish)
    cutR = 40.0 # Red color curve adjustement
    cutB = 20.0 # Blue color curve adjustment
    colR = 0.0
    colG = 0.0
    colB = 0.0
    tmpT = temperature
    # RED
    if tmpT < (baseTemp + cutR) :
        x = abs(tmpT - (baseTemp + cutR))
        # colR = 255 - 8.5 * x
        colR = 255 - 0.16 * x ** 2
        if colR < 0:
            colR = 0
    else :
        colR = 255
    
    # GREEN
    if tmpT == baseTemp :
        colG = 255
    elif tmpT > baseTemp :
        x = abs(tmpT - baseTemp)
        # colG = 255 - 3.0 * x
        colG = 255 - 0.25 * x ** 2
        if colG < 0 :
            colG = 0
    else :
        x = abs(tmpT - baseTemp)
        colG = 255 - 10.0 * x
        if colG < 0 :
            colG = 0

    # BLUE
    if tmpT > (baseTemp - cutB):
        x = abs(tmpT - (baseTemp - cutB))
        colB = 255 - 13.0 * x
        if colB < 0:
            colB = 0
    else :
        colB = 255
    
    return (int(colR), int(colG), int(colB))

# Define test function showin the temperature scale in color 
def showColorScale():
    global CurMode
    global CurColor
    for i in range(100):
        print(i)
        CurColor = fncTemperatureColor(i)
        pixels.fill(CurColor)
        j = i // 10
        if j & 8:
            pixels[14] = (255,255,255)
        else:
            pixels[14] = (0,0,0)
        
        if j & 4:
            pixels[15] = (255,255,255)
        else:
            pixels[15] = (0,0,0)

        if j & 2:
            pixels[16] = (255,255,255)
        else:
            pixels[16] = (0,0,0)

        if j & 1:
            pixels[17] = (255,255,255)
        else:
            pixels[17] = (0,0,0)
        pixels.show()
        time.sleep(0.5)
    time.sleep(0.5)
    pixelsOff()



# Define on_publish event function
def on_publish(client, userdata, mid):
    print("Message Published...")

# Define on_connect event function
def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC)
#    client.publish(MQTT_TOPIC, MQTT_MSG)

def on_message(client, userdata, msg):
    global CurTemp
    global CurMode
    global CurColor
    global pixels 
    payload = json.loads(msg.payload) # you can use json.loads to convert string to json
    if "temperature" in payload and CurMode == "temperature":
        NewTemp = payload['temperature']['temp']
        print(NewTemp) # then you can check the value
        if NewTemp != CurTemp:
            CurColor = fncTemperatureColor(NewTemp)
            pixels.fill(CurColor)
            #pixels[15] = (0,0,255) # Blue 
            #pixels[16] = (0,255,0) # Green
            #pixels[17] = (255,0,0) # Red 
            pixels.show()
            print("temp updated ", CurColor)
            CurTemp = NewTemp
            

    if "colorRGB" in payload and CurMode == "colorRGB":
        NewColor = payload['colorRGB']
        pixels.fill(NewColor)
        pixels.show()
        CurColor = NewColor
        print("Color updated ",NewColor)

    if "setMode" in payload:
        pixelsOff()
        CurMode = payload['setMode']['newMode']
        print("Mode changed to ",CurMode)
        if CurMode == 'showColorScale':
            showColorScale()

    if "getStatus" in payload:
        MQTT_MSG = json.dumps({"dutzoStatus": {"currentMode": CurMode,"currentColor": CurColor}})
        client.publish(MQTT_TOPIC, MQTT_MSG)


    
# NeoPixels must be connected to D18.
dutzo_controller_pin = board.D18
_pin = board.D18
# The number of NeoPixels
_pixels = 18
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
# pixels = neopixel.NeoPixel(dutzo_controller_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
pixels = neopixel.NeoPixel(_pin, _pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
pixels.fill((0,0,0))
pixels.show()
time.sleep(1)

# Initiate MQTT Client
client = mqtt.Client()
# Register publish callback function
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
# Connect with MQTT Broker
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
# Tell program to stay in this loop waiting for MQTT messages forever
client.loop_forever() 

# while True:
    # pass 
    # for j in range(num_pixels):
        # pixels[j] = (255,255,255)
        # pixels.show()
        # time.sleep(2)
        # pixels.fill((0,0,0))
    # pixels.fill((255, 0, 0))
    # pixels.show()
    # time.sleep(1)

    # pixels.fill((0, 255, 0))
    # pixels.show()
    # time.sleep(1)

    # pixels.fill((0, 0, 255))
    # pixels.show()
    # time.sleep(1)

    # pixels.fill((0, 0, 0))
    # pixels.show()
    # time.sleep(1)

