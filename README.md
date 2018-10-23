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