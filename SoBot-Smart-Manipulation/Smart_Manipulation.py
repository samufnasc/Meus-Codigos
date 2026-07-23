"""
Solis Robot - SoBot

MultiProg.py:  Programming example to control the SoBot
using a Logitech F710 controller, enabling the robot to follow 
a line and manipulate objects with its robotic arm integrated 
with computer vision.

Created By   : Vinicius M. Kawakami and Rodrigo L. de Carvalho
Version      : 2.0

Company: Solis Tecnologia
"""

import serial
import queue
from time import sleep
import threading
import signal
import sys
from read_gamepad import Read_Gamepad
from read_line import Read_Line
from aux_functions import *


# Function to handle script termination signal
def handle_signal(signum, frame):
    #dType.DisconnectDobot(api)
    usb.write(b"MT0 ME0")   # Disable motors
    usb.write(b"LT E0")     # Turn off Led Tap
    sys.exit(0)             # End the script

'''
###################################
        Main function
###################################
'''
if __name__ == '__main__':
    
    Desc_SoBot_serial = "VCOM"

    # Serial connection of the SoBot power and control board
    usb = serial.Serial()
    serial_SoBot = serial_device_finder(Desc_SoBot_serial)

    if serial_SoBot :
        # Connect to the found device
        usb = serial.Serial(serial_SoBot, baudrate=57600, timeout=1, dsrdtr=False)
        usb.flush()
        print(f"Connected to device: {serial_SoBot}")
    else:
        print("No device 0 was connected.")

    # Function registration for handling "SIGTERM" and "SIGINT" signal
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    #Configure return commands
    usb.write(b"CR1")
    usb.write(b"LT CR0")
    usb.write(b"MT0 CR0")
    usb.write(b"WP CR0")
    usb.write(b"DL CR1")
    usb.readline() 
    sleep(0.1)

    # Configure wheel parametres
    usb.write(b"WP MT1 WD100,05")
    usb.write(b"WP MT2 WD100,05")
    usb.write(b"WP DW268,65")

    # Set the motion proportional gain
    #usb.write(b"PG SO2,3 CA3,22 DF6,11 RI-6")

    # Configure operating parametres in continuous mode
    usb.write(b"MT0 MC MD0 AT100 DT100 V10")

    usb.write(b"LT E1 RD0 GR100 BL0")   # Turn on Led Tap

    #Configure threadings variables
    ev_read_line = threading.Event() 
    wait = threading.Event()
    read_serial_th = threading.Event()

    commands_queue = queue.Queue()

    #Configure threadings  
    app_Read_Serial = threading.Thread(target=Read_Serial, args=(read_serial_th, usb, wait, commands_queue))
    app_Read_Gamepad = threading.Thread(target=Read_Gamepad, args=(ev_read_line, usb))
    app_Read_Line = threading.Thread(target=Read_Line, args=(ev_read_line, usb, read_serial_th, commands_queue, wait))

    #Start threadings
    app_Read_Serial.start()
    app_Read_Gamepad.start()
    app_Read_Line.start()

# Let CTRL+C actually exit