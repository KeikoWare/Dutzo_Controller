
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
# Define color table for temperature scale -10 <-> 100 degree celcius
def fncTemperatureColor(temperature):
    baseTemp = 25.0
    colR = 0.0
    colG = 0.0
    colB = 0.0
    tmpT = float(temperature)
    # RED
    if tmpT < baseTemp :
        x = abs(tmpT - baseTemp)
        colR = 244 * ( x ** -0.133)
        if colR < 0:
            colR = 0
        if colR > 255:
            colR = 255
    else :
        colR = 255
    
    # GREEN
    if tmpT >= baseTemp :
        x = abs(tmpT - baseTemp)
        colR = -0.07 * (x ** 2) + 255
        if colG < 0 :
            colG = 0
    else :
        x = abs(tmpT - baseTemp)
        colR = -0.2 * (x ** 2) + 255
        if colG < 0 :
            colG = 0

    # BLUE
    if tmpT > baseTemp :
        x = abs(tmpT - baseTemp)
        colB = -0.25 * ( x ** 2) + 255
        if colB < 0:
            colB = 0
    else :
        colB = 255
    
    
    return (int(colR), int(colG), int(colB))

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
    payload = json.loads(msg.payload) # you can use json.loads to convert string to json
    if "temperature" in payload and CurMode == "temperature":
        NewTemp = payload['temperature']['temp']
        print(NewTemp) # then you can check the value
        if NewTemp != CurTemp:
            CurColor = fncTemperatureColor(temperature)
            pixels.fill(CurColor)
            pixels.show()
            CurTemp = NewTemp
            print("temp updated")

    if "colorRGB" in payload and CurMode == "colorRGB":
        NewColor = payload['colorRGB']
        if CurColor != NewColor:
            pixels.fill(NewColor)
            pixels.show()
            CurColor = NewColor
            print("Color updated")

    if "setMode" in payload:
        CurMode = payload['setMode']['newMode']
        print("Mode changed to ",CurMode)


# NeoPixels must be connected to D18.
dutzo_controller_pin = board.D18
# The number of NeoPixels
num_pixels = 18
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(dutzo_controller_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
pixels.fill((0,0,0))

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

