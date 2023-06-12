from flask import Flask, render_template, jsonify, send_file
import threading
from smbus import SMBus # (package python3-smbus) to read I2C
from ctypes import c_int16 # to read unsigned int as signed int
from time import time_ns, sleep
from gpiozero import LED, Button, DigitalInputDevice, DigitalOutputDevice
import pandas as pd

app= Flask(__name__)

GPIO_LED         = 17
GPIO_BUTTON      = 15
GPIO_MOTOR_START = 20
GPIO_MOTOR_READY = 21

DEVICE_BUS         =    1
DEVICE_ADDR        = 0x22
START_COUNTING     = 0x01
STOP_COUNTING      = 0x10
READ_LEFT_ENCODER  = 0x31
READ_RIGHT_ENCODER = 0x32
STEP_PER_360_DEGREE = 2048
DEGREE_PER_STEP = 360/STEP_PER_360_DEGREE

i2c = SMBus(DEVICE_BUS)
led = LED(GPIO_LED)
button = Button(GPIO_BUTTON, bounce_time=1)
motor_start = DigitalOutputDevice(GPIO_MOTOR_START, active_high=True, initial_value=False)
motor_ready = DigitalInputDevice(GPIO_MOTOR_READY)

while True :
    if button.is_pressed :
        led.on()
