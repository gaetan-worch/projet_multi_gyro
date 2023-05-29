from smbus import SMBus # (package python3-smbus) to read I2C
from ctypes import c_int16 # to read unsigned int as signed int
from time import time_ns, sleep
from gpiozero import LED, Button, DigitalInputDevice, DigitalOutputDevice

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

while True :
    if state == "WAIT_START_SIGNAL" :
        if button.is_pressed :
            motor_start.on()
            sleep(1)
            state = "START_MOTOR"

    elif state == "START_MOTOR" :
        if motor_ready.is_active :
            led.on()
            with open("measure.csv", "w") as file :
                file.write("Temps [ms],Capt. gauche,Capt. droite\n")
            print("Début de mesure")
            i2c.write_byte_data(DEVICE_ADDR, 0x00, START_COUNTING)
            start_time_ns = time_ns()
            state = "MEASURING"
        
    elif state == "MEASURING" :
        current_time_ms = (time_ns() - start_time_ns)/1e6
        angle_left = DEGREE_PER_STEP*c_int16(i2c.read_word_data(DEVICE_ADDR, READ_LEFT_ENCODER)).value
        angle_right = DEGREE_PER_STEP*c_int16(i2c.read_word_data(DEVICE_ADDR, READ_RIGHT_ENCODER)).value

        with open("measure.csv", "a") as file :
            file.write("%d,%.15g,%.15g\n" % (current_time_ms, angle_left, angle_right))

        sleep(0.1)

        if button.is_pressed :
            motor_start.off()
            led.off()
            print("Fin de mesure")
            i2c.write_byte_data(DEVICE_ADDR, 0x00, STOP_COUNTING)
            sleep(1) # pourquoi nécessaire ?
            state = "WAIT_START_SIGNAL"