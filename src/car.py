# import RPi.GPIO as GPIO
from time import sleep


class Car:
    keyUp = False
    keyDown = False
    keyLeft = False
    keyRight = False
    loop = True

    def __init__(self):
        print("Car init")
        while self.loop:
            self.gameLoop()
            sleep(1)  # 100ms

    def gameLoop(self):
        if self.keyUp and self.keyDown:
            self.keyUp = False
            self.keyDown = False

        if self.keyLeft and self.keyRight:
            self.keyLeft = False
            self.keyRight = False

        if not (self.keyUp and self.keyDown and self.keyLeft and self.keyRight):
            print("Stop all engines")
            return 0

        if self.keyUp:
            print("Car forward")
        elif self.keyDown:
            print("Car forward")
        else:
            print("Stop move engine")

        if self.keyLeft:
            print("Car turn left")
        elif self.keyRight:
            print("Car turn right")
        else:
            print("Stop rotate engine")


    def changeState(self, key, value):
        if key == 'ArrowUp':
            self.keyUp = value
        elif key == 'ArrowDown':
            self.keyDown = value
        elif key == 'ArrowLeft':
            self.keyLeft = value
        elif key == 'ArrowRight':
            self.keyRight = value
