#!/usr/bin/python2.7
import RPi.GPIO as GPIO
import subprocess as SP
GPIO.setmode(GPIO.BCM)

GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    GPIO.wait_for_edge(15, GPIO.FALLING) 
    SP.call(['sudo','shutdown','-h','now'])
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit