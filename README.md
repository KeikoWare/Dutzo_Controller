# Dutzo_Controller

sudo apt-get install git
git config --global user.email "keiko@keikoware.dk"
git config --global user.name "KeikoWare"

sudo apt-get install python3-pip
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka

sudo pip3 install flask # Dont need it

sudo apt-get install mosquitto mosquitto-clients

sudo pip3 install paho-mqtt


COMMANDS:
{"setMode": {"newMode": "colorRGB"}}
{"setMode": {"newMode": "temperature"}}
{"colorRGB": [0,128,128]}
{"temperature": {"temp": 23.25,"humidity": 65.5,"tempScale": "celcius"}}


$ nohup sudo python3 raspberrypi_dustzo_controller/MQTT_temperature_publish.py &
$ sudo python3 raspberrypi_dustzo_controller/MQTT_Dutzo_controller.py
