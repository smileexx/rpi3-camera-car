# rpi3-camera-car

This is my <del>(very first time)</del> first Python project. 
And some else technologies like websocket and ffmpeg also new for me.

Main goal of this project is to build RC car :oncoming_police_car: to annoying my cat while it stay alone.
So "car" should controlled through WiFi and stream live from cam. 



As a base for WebSocket server I use this small project
https://github.com/sanketplus/PyWSocket
with modified method `decode_frame`.



### Client side

In `main.js` set up a WebSocket server address `ws://192.168.0.101:46464`. This is an address of my Raspberry Pi in LAN.

We use method `Game::encode` for make a 'bit mask' representation of our control keys state and encode it to int.

For example, forward command (ArrowUp) will be a value = `'100000'` and than encoded to int = `32`.



### Server 

Server will contains at least three different subjects:

1. ffmpeg & ffserver for streaming live from webcam
2. WebSocket server and handling signals from client
3. Manage hardware with GPOI


### Streaming video
I'm using old USB webcam. Folder `camera` in project contains simple config for ffserver and script for run/stop ffmpeg.     


## Some tips and notes 

#### Info about GPIO pins
GPOI Docs: 
* https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

PWM:
* https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
* https://www.mbtechworks.com/projects/raspberry-pi-pwm.html



#### Info about WiFi config

> This tips for Raspbian Stretch

* https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
* https://raspberrypi.stackexchange.com/questions/39785/dhcpcd-vs-etc-network-interfaces

It works for me. Don't touch file `/etc/network/interfaces`. 
Use `/etc/dhcpcd.conf` and `/etc/wpa_supplicant/wpa_supplicant.conf` for configure.

Also you maybe need to reboot RPi because restarting dhcpcd & networking does not work wor me.