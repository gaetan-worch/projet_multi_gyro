from flask import Flask
from flask import render_template
import RPi.GPIO as rpi
import time
import threading

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
motor_ready = DigitalInputDevice(GPIO_MOTOR_READY, pull_up=True)

state = "WAIT_START_SIGNAL"

mesure_thread = None

def startMotor() :
    while not motor_ready.is_active :
        sleep(1)
    state = "MEASURING"

def mesureLoop() :
    startMotor()
    while(state == "MEASURING") :
        #Code Mesure    
        sleep(1)  

@app.route('/demmarreMesure', methods=['POST'])
def demarrerMesure() :
    if (state == "WAIT_START_SIGNAL"):
        state = "START_MOTOR"
        motor_start.on()
        mesure_thread = threading.Thread(target=mesureLoop)
        mesure_thread.start()


@app.route("/stopMesure")
def stopMesure() :
    if(state != "WAIT_START_SIGNAL") :
        state = "WAIT_START_SIGNAL"
        mesure_thread.join()
        
if __name__=="__main__":
    print("Start")
    app.run(debug=True, host='MON_IP')
