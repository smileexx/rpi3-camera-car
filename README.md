# rpi3-camera-car

This is my <del>(very first time)</del> first Python project.

:oncoming_police_car:


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



#### Some useful info
GPOI Docs: https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

PWM:

https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
https://www.mbtechworks.com/projects/raspberry-pi-pwm.html
