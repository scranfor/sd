#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import datetime

debug1 = False
debug2 = False

# Class sd implements methods to send step-and-direction signals from a Raspberry Pi to a motion controller
class sd:

  # Define clockwise and counterclockwise logic levels
  CW = GPIO.HIGH
  CCW = GPIO.LOW

  def __init__(self, stepsPerRev, stepPin, dirPin, enablePin):
    self.stepsPerRev = stepsPerRev
    self.stepPin = stepPin
    self.dirPin = dirPin
    self.enablePin = enablePin
    self.position = 0 # This is our absolute position in steps
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.stepPin, GPIO.OUT)
    GPIO.setup(self.dirPin, GPIO.OUT)
    GPIO.setup(self.enablePin, GPIO.OUT)
    GPIO.output(self.stepPin, GPIO.LOW)
    GPIO.output(self.dirPin, GPIO.LOW)
    GPIO.output(self.enablePin, GPIO.HIGH)
    # stepIntervalWork is currently just a magic number that I precomputed on my Raspberry Pi 3 running Raspbian and python 3
    # This value is dependent on the hardware, OS, and version of Python you use
    # It should be set to minimize the value of (catchUps + slowDowns), ie resulting in the most stable interval between steps and so the smoothest motion
    # In future versions, we might be able to compute this value, perhaps at time of instantiation.
    # stepInvervalWork is also an absolute lower limit of stepInterval, otherwise we'll start calling sleep() with negative values...
    self.stepIntervalWork = 0.00009

    if debug1:
      print("Instantiation info:")
      print("  stepsPerRev: " + str(self.stepsPerRev))
      print("  stepPin: " + str(self.stepPin))
      print("  dirPin: " + str(self.dirPin))
      print("  enablePin: " + str(self.enablePin))

  def cleanup(self):
    GPIO.output(self.enablePin, GPIO.LOW)
    GPIO.cleanup()

  def step(self, steps, direction, rpm):
    GPIO.output(self.dirPin, direction)

    positionMultiplier = 1
    if direction == self.CCW:
      positionMultiplier = -1

    # How many seconds to wait between steps, from rising edge to rising edge
    stepInterval = 60 / ( rpm * self.stepsPerRev )

    elapsedSteps = 0
    catchUps = 0
    slowDowns = 0
    startTime = datetime.datetime.now()
    stepIntervalSleep = stepInterval - self.stepIntervalWork

    while elapsedSteps < steps:
      thisStep = datetime.datetime.now()
      GPIO.output(self.stepPin, GPIO.HIGH) # Pulse the step pin
      GPIO.output(self.stepPin, GPIO.LOW)
      elapsedSteps += 1
      self.position += (1 * positionMultiplier) # Keep track of our absolute position

      # How many steps SHOULD we have taken by now?
      computedSteps = int((1 + (thisStep - startTime) / datetime.timedelta(microseconds=stepInterval * 1000000)))

      sleepTime = stepIntervalSleep

      if computedSteps > elapsedSteps:
        sleepTime = stepIntervalSleep * 0.85
        catchUps += 1 # catchUps are common
        if debug2: print ("      catch up!")

      if computedSteps < elapsedSteps:
        sleepTime = stepIntervalSleep * 1.15
        slowDowns += 1 # slowDowns are rare
        if debug2: print ("      slow down!")

      sleep(sleepTime)

      if debug2:
        print ("computedSteps: " + str(computedSteps))
        print ("elapsedSteps: " + str(elapsedSteps))
        print ()

    if debug1:
      endTime = datetime.datetime.now()
      print("Pre-step() info:")
      print("  steps: " + str(steps))
      print("  stepInterval: " + str(stepInterval))
      print("  Calculated time: " + str(steps * stepInterval))
      print("Post-step() info:")
      print("  Elapsed time: " + str(endTime - startTime)) 
      print("  catchUps: " + str(catchUps))
      print("  slowDowns: " + str(slowDowns))
