import RPi.GPIO as GPIO
import threading
from time import sleep
import socketserver as SocketServer
from server import MyTCPHandler

lock = threading.Lock()

MM_L_PIN = 17    # Move motor level pin PWM

class Car:
    MM = None
    MM_DC = 0
    
    key_up = False
    key_down = False
    key_left = False
    key_right = False
    loop = True

    mask = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Shift", "Control"]

    def __init__(self):
        print("init hardware")
        self.init_pins()
        
        print("init server")
        server_address = ("0.0.0.0", 46464)
        server = SocketServer.TCPServer(server_address, MyTCPHandler)
        server._car = self
        self._server = server
        
        print("init car")
        self.run_server()
        self.run()
        
    def run(self):
        print("Car run")
        while self.loop:
            try:
                self.game_loop()
                sleep(0.1)  # 100ms
            except KeyboardInterrupt:
                self.loop = False
                self.reset_gpio()
                return 0
            except Exception as ex:
                print("ERROR in Car loop. %s" % ex)
                self.reset_gpio()

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
            self.move_motor()
            return 0

        if self.key_up:
            print("Car forward")
            self.move_motor(1)
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
       
    def init_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)        
        
        GPIO.setup(MM_L_PIN, GPIO.OUT)
        self.MM = GPIO.PWM(MM_L_PIN, 100)
       
    def reset_gpio(self):
        GPIO.cleanup()
       
    def move_motor(self, pow = 0):
        if pow:
            if self.MM_DC <= 10:
                self.MM_DC = 20
                self.MM.start(10)
                sleep(0.2)
            elif self.MM_DC <= 20:
                self.MM_DC = 50
                self.MM.start(20)
                sleep(0.2)
            else:
                self.MM.ChangeDutyCycle(self.MM_DC)
        else:
            self.MM_DC = 0
            self.MM.stop()

    