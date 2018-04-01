#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import datetime

from sd import sd

if __name__ == '__main__':     # Program start from here
  try:
    print("Use Ctrl + C to stop")
    motor = sd(800, 12, 3, 5)
    motor.step(10000, sd.CW, 100)
    print("Position: " + str(motor.position))
    motor.step(100, sd.CCW, 100)
    print("Position: " + str(motor.position))
    motor.step(200, sd.CW, 100)
    print("Position: " + str(motor.position))
  except KeyboardInterrupt:  # When 'Ctrl+C' is pressed
    motor.cleanup()
    print("")
