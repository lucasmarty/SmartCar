#!/usr/bin/python

from __future__ import print_function
import time
import RPi.GPIO as GPIO

from threading import Thread

# -----------------------
# Define sensor parameters
# -----------------------

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

# Speed of sound in cm/s at temperature
temperature = 20
speedSound = 33100 + (0.6*temperature)


# -----------------------
# Define measurement functions
# -----------------------
def measure():
  # This function measures a distance
  GPIO.output(GPIO_TRIGGER, True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * speedSound)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.

  distance1=measure()
  time.sleep(0.1)
  distance2=measure()
  time.sleep(0.1)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

def setup():
  # Use BCM GPIO references
  # instead of physical pin numbers
  GPIO.setmode(GPIO.BCM)

  print("Ultrasonic measurement setup:")
  print("Speed of sound is",speedSound/100,"m/s at ",temperature,"deg")

  # Set pins as output and input
  GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
  GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

  # Set trigger to False (Low)
  GPIO.output(GPIO_TRIGGER, False)

  # Allow module to settle
  time.sleep(0.5)


def run(sleep_time=1):
  # Wrap main content in a try block so we can
  # catch the user pressing CTRL-C and run the
  # GPIO cleanup function. This will also prevent
  # the user seeing lots of unnecessary error
  # messages.
  try:
    while True:
      distance = measure_average() # takes ~0.2 seconds
      print("Distance : {0:5.1f}".format(distance))
      time.sleep(sleep_time)

  except KeyboardInterrupt:
    # User pressed CTRL-C
    # Reset GPIO settings
    GPIO.cleanup()

class UltrasonicAsync(Thread):
  def __init__(self, sleep_time):
    Thread.__init__(self)
    self.dist = measure_average()
    # Add config code here

  def run(self):
    while True:
      dist = measure_average()
      self.dist = dist

  # Safe stop method here

