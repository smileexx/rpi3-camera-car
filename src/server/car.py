import RPi.GPIO as GPIO
import threading
from time import sleep
import socketserver as SocketServer
from server import MyTCPHandler

lock = threading.Lock()

# DM - Drive Move pins
PIN_DM_SIGNAL = 22
PIN_L_FWD = 17  # pin to move forward
PIN_L_BW = 27  # to move backward

# DR - Drive Rotate pins
PIN_DR_SIGNAL = 13
PIN_R_FWD = 5  # pin to turn left
PIN_R_BW = 6  # turn right

MOTOR_FREQ = 70
MOTOR_DC = 80


class Car:
    DM_PWM = None
    DR_PWM = None

    lm_state = False
    rm_state = False

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
            self.left_motor(False)
            self.right_motor(False)
            return 0

        if self.key_up:
            print("Car forward")
            self.left_motor(True)
            self.right_motor(True)
        elif self.key_down:
            print("Car move back")
            self.left_motor(True, False)
            self.right_motor(True, False)
        elif not (self.key_up or self.key_down):
            self.left_motor(False)
            self.right_motor(False)

        # if self.key_left:
        #     print("Car turn left")
        #     self.right_motor(True)
        # elif self.key_right:
        #     print("Car turn right")
        #     self.left_motor(True)
        # elif not(self.key_left or self.key_right):
        #     self.left_motor(False)
        #     self.right_motor(False)

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
        chan_list = [PIN_DM_SIGNAL, PIN_L_FWD, PIN_L_BW, PIN_DR_SIGNAL, PIN_R_FWD, PIN_R_BW]
        GPIO.setup(chan_list, GPIO.OUT)  # init all pins as OUT

        # init PWM
        self.DM_PWM = GPIO.PWM(PIN_DM_SIGNAL, MOTOR_FREQ)  # frequency=50Hz
        self.DM_PWM.start(0)

        self.DR_PWM = GPIO.PWM(PIN_DR_SIGNAL, MOTOR_FREQ)  # frequency=50Hz
        self.DR_PWM.start(0)

    def reset_gpio(self):
        try:
            GPIO.cleanup()
        except:
            print("Nothing to clear in GPIO")
            pass

    def left_motor(self, power=False, forward=True):
        if power and not self.lm_state:
            self.lm_state = True
            if forward:
                print('Left FWD')
                GPIO.output(PIN_L_FWD, GPIO.HIGH)
                GPIO.output(PIN_L_BW, GPIO.LOW)
            else:
                print('Left BW')
                GPIO.output(PIN_L_FWD, GPIO.LOW)
                GPIO.output(PIN_L_BW, GPIO.HIGH)
            self.DM_PWM.start(MOTOR_DC)
        elif not power and self.lm_state:
            GPIO.output(PIN_L_FWD, GPIO.LOW)
            GPIO.output(PIN_L_BW, GPIO.LOW)
            self.DM_PWM.ChangeDutyCycle(0)
            self.DM_PWM.stop()
            self.lm_state = False
            print('stop Left')

    def right_motor(self, power=False, forward=True):
        if power and not self.rm_state:
            self.rm_state = True
            if forward:
                print('Right FWD')
                GPIO.output(PIN_R_FWD, GPIO.HIGH)
                GPIO.output(PIN_R_BW, GPIO.LOW)
            else:
                print('Right BW')
                GPIO.output(PIN_R_FWD, GPIO.LOW)
                GPIO.output(PIN_R_BW, GPIO.HIGH)
            self.DM_PWM.start(MOTOR_DC)
        elif not power and self.rm_state:
            GPIO.output(PIN_R_FWD, GPIO.LOW)
            GPIO.output(PIN_R_BW, GPIO.LOW)
            self.DM_PWM.ChangeDutyCycle(0)
            self.DM_PWM.stop()
            self.rm_state = False
            print('stop Right')


    #
    # def move_motor(self, power=False, forward=True):
    #     if power and not self.lm_state:
    #         self.lm_state = True
    #         if forward:
    #             print('FWD')
    #             GPIO.output(PIN_L_FWD, GPIO.HIGH)
    #             GPIO.output(PIN_L_BW, GPIO.LOW)
    #         else:
    #             print('BW')
    #             GPIO.output(PIN_L_FWD, GPIO.LOW)
    #             GPIO.output(PIN_L_BW, GPIO.HIGH)
    #         self.DM_PWM.start(MOTOR_DC)
    #     elif not power and self.lm_state:
    #         GPIO.output(PIN_L_FWD, GPIO.LOW)
    #         GPIO.output(PIN_L_BW, GPIO.LOW)
    #         self.DM_PWM.ChangeDutyCycle(0)
    #         self.DM_PWM.stop()
    #         self.lm_state = False
    #         print('stop move')
    #
    # def rotate_motor(self, power=False, left=True):
    #     if power and not self.dr_state:
    #         self.dr_state = True
    #         if left:
    #             GPIO.output(PIN_R_FWD, GPIO.HIGH)
    #             GPIO.output(PIN_R_BW, GPIO.LOW)
    #         else:
    #             GPIO.output(PIN_R_FWD, GPIO.LOW)
    #             GPIO.output(PIN_R_BW, GPIO.HIGH)
    #         self.DR_PWM.ChangeDutyCycle(100)
    #     elif not power and self.dr_state:
    #         GPIO.output(PIN_R_FWD, GPIO.LOW)
    #         GPIO.output(PIN_R_BW, GPIO.LOW)
    #         self.DR_PWM.ChangeDutyCycle(0)
    #         self.DR_PWM.stop()
    #         self.dr_state = False
    #         print('stop rotate')
