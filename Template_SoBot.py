#!/usr/bin/python3
"""
Solis Robot - SoBot

Templete_SoBot.py: Template Program to the SoBot.

Created By   : Vinicius M. Kawakami
Version      : 1.0

Company: Solis Tecnologia
"""
import serial

# Configures the serial port
usb = serial.Serial('/dev/ttyACM0', 57600, timeout=0, dsrdtr=False)
usb.flush()

# Configures the wheel parameters
usb.write(b"WP MT1 WD100")
usb.write(b"WP MT2 WD100")

# Sets the proportional gain for movement control
usb.write(b"PG SO2,3 CA3,22 DF6,11 RI-6")
