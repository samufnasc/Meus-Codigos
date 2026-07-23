#!/usr/bin/python3
"""
Solis Robot - SoBot

Simple-Route.py: Programming example for the SoBot to move a simple route.

Created By   : Vinicius M. Kawakami
Version      : 1.0

Company: Solis Tecnologia
"""

from time import sleep
import serial

# Set serial port
usb = serial.Serial('/dev/ttyACM0', 9600, timeout=0, dsrdtr=False)
usb.flush()     # Waits data configuration

usb.write(b"LT E1 RD50 GR0 BL0")    # Turn on led tape in red

usb.write(b"MT0 E1")                # Enables wheel motors

sleep(0.1)

usb.write(b"MT0 E1 D1000 AT5000 DT5000 V10")    # Move forward

usb.write(b"MT0 E1 D90 R AT3950 DT3950 V10")    # Move 90° to the right

usb.write(b"MT0 E1 D1000 AT5000 DT5000 V10")    # Move forward

usb.write(b"MT0 E1 D90 L AT3950 DT3950 V10")    # Move 90° to the left

usb.write(b"MT0 E1 D1000 AT5000 DT5000 V10")    # Move forward

usb.write(b"LT E1 RD0 GR0 BL0")    # Turn off led tape

usb.write(b"MT0 E0")                # Disables wheel motors