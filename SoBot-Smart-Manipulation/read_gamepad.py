"""
Controller button functions:
BTN_X – Configure LED Strip in Blue color
BTN_Y – Configure LED Strip in Yellow color
BTN_A – Configure LED Strip in Green color
BTN_B – Configure LED Strip in Red color
BTN_START – Enables wheel motors
BTN_BACK – Enable and Disables line follower mode
BTN_R1 – Configure curve mode on the same axis
BTN_L1 – Configure differential curve mode
BTN_R2 – Sets speed 10cm/s
BTN_L2 – Sets speed 4cm/s
BTN_UP – Moves the robot forward
BTN_DOWN – Moves the robot backwards
BTN_LEFT – Moves the robot to the left
BTN_RIGTH – Moves the robot to the right

Code explain: https://youtu.be/6aBEMOffvbQ?si=iRRhLpEAoaR9QXHz
"""

import inputs
import threading

flag_BTX_press = 0
flag_BTY_press = 0
flag_pause = 0

def Timer_BTX_Press ():
    global flag_BTX_press
    flag_BTX_press = 0

def Timer_BTY_Press ():
    global flag_BTY_press
    flag_BTY_press = 0

def Timer_Pause (usb):
    global flag_pause
    global flag_BTX_press
    global flag_BTY_press

    flag_pause = 0

    if flag_BTY_press == 2:
        usb.write(b"MT0 MP")
        threading.Timer(0.1, Timer_BTY_Press).start()
    elif flag_BTX_press == 2:
        usb.write(b"MT0 MP")
        threading.Timer(0.1, Timer_BTX_Press).start()


'''
###################################
Function created to read Logitech control commands
###################################
'''
def Read_Gamepad(ev_read_line, usb):
    global flag_pause
    global flag_BTX_press
    global flag_BTY_press

    flag_start = 0
    flag_vel = 1
    flag_BT_RZ = 0
    flag_BT_Z = 0

    # Find the Logitech F710 controller ID connected to the Raspberry Pi
    gamepad = inputs.devices.gamepads[0]
    print(gamepad)


    while True:
        
        events = inputs.get_gamepad()   # Checks if there was any control event
        #print(f"Eventos: {events}")

        for event in events:
            
            # Checks if it is event of type "KEY"
            if event.ev_type == "Key":
                #print(f"Evento code: {event.code}")
                #print(f"Evento state: {event.state}")

                # Check if the event code is "BTN_SELECT" in state 1
                if event.code == "BTN_SELECT":
                    if ev_read_line.is_set() == 0 and event.state == 1:
                        print("SELECT button pressed")
                        usb.write(b"LT E1 RD100 GR100 BL100")       # Turn on Led Tap
                        usb.write(b"MT0 MC MD1 RI20 AT50 DT50 V10")  # Parameter settings for continuous mode
                        usb.write(b"MT0 ME1")                       # Enables wheel motors on mode continuous
                        print("LINE FOLLOWER MODE ACTIVATED")
                        ev_read_line.set()

                    elif ev_read_line.is_set() and event.state == 1:
                        print("SELECT button pressed")
                        usb.write(b"MT0 MP")                # Moviment Pause
                        usb.write(b"MT0 ME0")

                        print("LINE FOLLOWER MODE DEACTIVATED")
                        ev_read_line.clear()

                if  ev_read_line.is_set() == 0 :
                    # Check if the event code is "BTN_START" in state 1
                    if event.code == "BTN_START" and event.state == 1:
                        print("START button pressed")
                        if flag_start == 0:
                            flag_start = 1
                            usb.write(b"MT0 ME1")               # Enable motors
                            usb.write(b"LT E1 RD0 GR0 BL100")   # Turn on Led Tap

                        else:
                            flag_start = 0
                            usb.write(b"MT0 ME0")               # Disable motors
                            usb.write(b"LT E1 RD0 GR100 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_SOUTH" in state 1
                    if event.code == "BTN_SOUTH" and event.state == 1:
                        print("A button pressed")
                        usb.write(b"LT E1 RD0 GR100 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_EAST" in state 1
                    elif event.code == "BTN_EAST" and event.state == 1:
                        print("B button pressed")
                        usb.write(b"LT E1 RD100 GR0 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_NORTH" in state 1
                    elif event.code == "BTN_NORTH" and event.state == 1:
                        print("X button pressed")
                        usb.write(b"LT E1 RD0 GR0 BL100")   # Turn on Led Tap

                    # Check if the event code is "BTN_WEST" in state 1
                    elif event.code == "BTN_WEST" and event.state == 1:
                        print("Y button pressed")
                        usb.write(b"LT E1 RD100 GR50 BL0")   # Turn on Led Tap

                    # Check if the event code is "BTN_TR" in state 1
                    elif event.code == "BTN_TR" and event.state == 1:
                        print("RB button pressed")
                        # Configure continuous mode with curve on the same axis
                        if flag_vel:
                            usb.write(b"MT0 MC MD0 AT100 DT100 V10")
                        else:
                            usb.write(b"MT0 MC MD0 AT100 DT100 V4")

                    # Check if the event code is "BTN_TL" in state 1
                    elif event.code == "BTN_TL" and event.state == 1:
                        print("LB button pressed")
                        # Configure continuous mode with differential curve
                        if flag_vel:
                            usb.write(b"MT0 MC MD1 RI100 AT100 DT100 V10")
                        else:
                            usb.write(b"MT0 MC MD1 RI100 AT100 DT100 V4")

            # Checks if it is event of type "Absolute"
            if event.ev_type == "Absolute":
                # print(f"Evento code: {event.code}")
                # print(f"Evento state: {event.state}")

                if ev_read_line.is_set() == 0:
                    ### Buttons to control the direction ###
                    # Events with the MODE button disabled
                    # Check if the event code is "ABS_HAT0X"
                    if event.code == "ABS_HAT0X":
                        if flag_start:                  # Check if flag_start is enable
                            if flag_BTY_press == 0 and flag_BTX_press == 0:
                                if event.state == -1:       # Check state (left direction) of the button
                                    flag_BTX_press = 1
                                    flag_pause = 1
                                    print("ESQ button pressed")
                                    usb.write(b"MT0 ML")
                                    threading.Timer(0, Timer_Pause, args=(usb,)).start()

                                elif event.state == 1:      # Check state (right direction) of the button
                                    flag_BTX_press = 1
                                    flag_pause = 1
                                    print("DIR button pressed")
                                    usb.write(b"MT0 MR")
                                    threading.Timer(0, Timer_Pause, args=(usb,)).start()
                                    
                                    print("DIR button pressed")

                            elif flag_BTX_press == 1:
                                if event.state == 0:
                                    flag_BTX_press = 2
                                    if flag_pause == 0:
                                        usb.write(b"MT0 MP")
                                        threading.Timer(0, Timer_BTX_Press).start()

                    # Check if the event code is "ABS_HAT0Y"
                    if event.code == "ABS_HAT0Y":
                        if flag_start:                  # Check if flag_start is enable
                            if flag_BTX_press == 0 and flag_BTY_press == 0:
                                if event.state == -1:       # Check state (front direction) of the button
                                    flag_BTY_press = 1
                                    flag_pause = 1
                                    print("FRONT button pressed")
                                    usb.write(b"MT0 MF")
                                    threading.Timer(0, Timer_Pause, args=(usb,)).start()

                                elif event.state == 1:      # Check state (back direction) of the button
                                    flag_BTY_press = 1
                                    flag_pause = 1
                                    print("BACK button pressed")
                                    usb.write(b"MT0 MB")
                                    threading.Timer(0, Timer_Pause, args=(usb,)).start()

                            elif flag_BTY_press == 1:
                                if event.state == 0:
                                    flag_BTY_press = 2
                                    if flag_pause == 0:
                                        usb.write(b"MT0 MP")
                                        threading.Timer(0, Timer_BTY_Press).start()
                    
                    ### Buttons to control the velocity ###
                    # Check if the event code is "ABS_RZ"
                    if event.code == "ABS_RZ":
                        if event.state >= 1:            # Check if state is greater than 1 (button pressed)
                            if flag_BT_RZ == 0:
                                flag_BT_RZ = 1
                                flag_vel = 1
                                print("RZ button pressed")
                                usb.write(b"MT0 MC MD0 AT100 DT100 V8")
                        elif event.state == 0:
                            print("RZ button released")
                            flag_BT_RZ = 0

                    # Check if the event code is "ABS_Z"
                    if event.code == "ABS_Z":
                        if event.state >= 1:            # Check if state is greater than 1 (button pressed)
                            if flag_BT_Z == 0:
                                flag_BT_Z = 1
                                flag_vel = 0
                                print("Z button pressed")
                                usb.write(b"MT0 MC MD0 AT100 DT100 V4")
                        elif event.state == 0:
                            print("Z button realeased")
                            flag_BT_Z = 0