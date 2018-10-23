# import RPi.GPIO as GPIO
import threading
from time import sleep
import socketserver as SocketServer
from server import MyTCPHandler

lock = threading.Lock()


class Car:
    key_up = False
    key_down = False
    key_left = False
    key_right = False
    loop = True

    mask = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Shift", "Control"]

    def __init__(self):
        server_address = ("0.0.0.0", 46464)
        server = SocketServer.TCPServer(server_address, MyTCPHandler)
        server._car = self
        self._server = server

        print("init car")
        self.reset_gpio()
        self.run_server()
        self.run()

    def reset_gpio(self):
        # reset all GPIO pins
        pass

    def run(self):
        print("Car run")
        while self.loop:
            try:
                self.game_loop()
                sleep(0.1)  # 100ms
            except KeyboardInterrupt:
                self.loop = False
                return 0
            except Exception as ex:
                print("ERROR in Car loop. %s" % ex)

    def run_server(self):
        print("Server run")

        t = threading.Thread(target=self._server.serve_forever)
        t.setDaemon(True)  # don't hang on exit
        t.start()

    def game_loop(self):
        if self.key_up and self.key_down:
            self.key_up = False
            self.key_down = False

        if self.key_left and self.key_right:
            self.key_left = False
            self.key_right = False

        if not (self.key_up or self.key_down or self.key_left or self.key_right):
            # print("Stop all engines")
            return 0

        if self.key_up:
            print("Car forward")
        elif self.key_down:
            print("Car move back")

        if self.key_left:
            print("Car turn left")
        elif self.key_right:
            print("Car turn right")

    def change_state(self, key, value):
        if key == 'ArrowUp':
            self.key_up = value
        elif key == 'ArrowDown':
            self.key_down = value
        elif key == 'ArrowLeft':
            self.key_left = value
        elif key == 'ArrowRight':
            self.key_right = value

    def parse_bit_state(self, data):
        print(data)
        lock.acquire()
        for index, key in enumerate(self.mask):
            self.change_state(key, bool(data[index] == '1'))
        lock.release()
