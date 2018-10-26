import RPi.GPIO as GPIO
import threading
from time import sleep
import socketserver as SocketServer
from server import MyTCPHandler

lock = threading.Lock()

# DM - Drive Move pins
PIN_DM_SIGNAL = 22
PIN_DM_FWD = 17  # pin to move forward
PIN_DM_BW = 27  # to move backward

# DR - Drive Rotate pins
PIN_DR_SIGNAL = 13
PIN_DR_L = 5  # pin to turn left
PIN_DR_R = 6  # turn right

MOTOR_FREQ = 50
MOTOR_DC = 50


class Car:
    DM_PWM = None
    DR_PWM = None

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
                print("Stop on KeyboardInterrupt")
                self.loop = False
                self.reset_gpio()
                return 0
            except Exception as ex:
                print("ERROR in Car loop. %s" % ex)
                self.loop = False
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
            self.move_motor(False)
            self.rotate_motor(False)
            return 0

        if self.key_up:
            print("Car forward")
            self.move_motor(True)
        elif self.key_down:
            print("Car move back")
            self.move_motor(True, False)

        if self.key_left:
            print("Car turn left")
            self.rotate_motor(True)
        elif self.key_right:
            print("Car turn right")
            self.rotate_motor(True, False)

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
        """Initialize all hardware here"""
        self.reset_gpio()
        GPIO.setmode(GPIO.BCM)  # Set pin numbers mode
        GPIO.setwarnings(False)  # Disable warning about pins in use
        chan_list = [PIN_DM_SIGNAL, PIN_DM_FWD, PIN_DM_BW, PIN_DR_SIGNAL, PIN_DR_L, PIN_DR_R]
        GPIO.setup(chan_list, GPIO.OUT)  # init all pins as OUT
        # init PWM
        self.DM_PWM = GPIO.PWM(PIN_DM_SIGNAL, MOTOR_FREQ)  # frequency=50Hz
        self.DR_PWM = GPIO.PWM(PIN_DR_SIGNAL, MOTOR_FREQ)  # frequency=50Hz

    def reset_gpio(self):
        try:
            GPIO.cleanup()
        except:
            print("Nothing to clear in GPIO")
            pass

    def move_motor(self, power=False, forward=True):
        if power:
            if forward:
                GPIO.output(PIN_DM_FWD, GPIO.HIGH)
                GPIO.output(PIN_DM_BW, GPIO.LOW)
            else:
                GPIO.output(PIN_DM_FWD, GPIO.LOW)
                GPIO.output(PIN_DM_BW, GPIO.HIGH)
            self.DM_PWM.start(MOTOR_DC)
        else:
            GPIO.output(PIN_DM_FWD, GPIO.LOW)
            GPIO.output(PIN_DM_BW, GPIO.LOW)
            self.DM_PWM.stop()

    def rotate_motor(self, power=False, left=True):
        if power:
            if left:
                GPIO.output(PIN_DR_L, GPIO.HIGH)
                GPIO.output(PIN_DR_R, GPIO.LOW)
            else:
                GPIO.output(PIN_DR_L, GPIO.LOW)
                GPIO.output(PIN_DR_R, GPIO.HIGH)
            self.DR_PWM.start(MOTOR_DC)
        else:
            GPIO.output(PIN_DR_L, GPIO.LOW)
            GPIO.output(PIN_DR_R, GPIO.LOW)
            self.DR_PWM.stop()
