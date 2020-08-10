import RPi.GPIO as GPIO
import time


class led_statement:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.RED = 7
        self.GREEN = 3
        self.BLUE = 5
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.output(self.RED, 0)
        GPIO.setup(self.GREEN, GPIO.OUT)
        GPIO.output(self.GREEN, 0)
        GPIO.setup(self.BLUE, GPIO.OUT)
        GPIO.output(self.BLUE, 0)

    def rgb(self, r, g, b):
        GPIO.output(self.RED, r)
        GPIO.output(self.GREEN, g)
        GPIO.output(self.BLUE, b)

    def cleanup(self, timer):
        time.sleep(timer)
        GPIO.cleanup()
