# Dutzo_Controller

sudo apt-get install git

git config --global user.email "keiko@keikoware.dk"

git config --global user.name "KeikoWare"

sudo apt-get install python3-pip

sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

sudo python3 -m pip install --force-reinstall adafruit-blinka

// sudo pip3 install flask // Dont need it

sudo apt-get install mosquitto mosquitto-clients

sudo pip3 install paho-mqtt


COMMANDS:

{"setMode": {"newMode": "colorRGB"}}

{"setMode": {"newMode": "temperature"}}

{"setMode": {"newMode": "showColorScale"}}

{"setMode": {"newMode": "pixelsOff"}}


{"colorRGB": [0,128,128]}

{"temperature": {"temp": 23.25,"humidity": 65.5,"tempScale": "celcius"}}

{"getStatus" : 1}

Commandline start temperature server:

$ nohup sudo python3 raspberrypi_dustzo_controller/MQTT_temperature_publish.py &

Commandline start Dutzo Controller:

$ sudo python3 raspberrypi_dustzo_controller/MQTT_Dutzo_controller.py
