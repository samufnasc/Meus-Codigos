
from time import sleep
import pygame
from aux_functions import *
import lib_arm.DobotDllType as dType

#Functin when stop read line
def stop_read_line (usb):
    usb.write(b"LT E1 RD0 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD50 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD0 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD50 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD0 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD50 GR0 BL0")
    sleep(0.5)
    usb.write(b"LT E1 RD0 GR0 BL0")
    usb.write(b"LT E0")
    sleep(0.5)
    usb.write(b"MT0 MC MD0 AT100 DT100 V8")
    usb.write(b"LT E1 RD0 GR100 BL0")   


'''
###################################
Function created to read the line sensor
###################################
'''
def Read_Line(ev_read_line, usb, read_serial_th, commands_queue, wait):

    times_exec = 0

    invert = False
    once_read_line = False
    black = 49
    white = 48

    flag_forward = 0
    flag_left = 0
    flag_right = 0
    state = 2
    count_bl = 0

    # Serial connection to the Magician Lite Arm
    api_arm = Connect_Dobot()

    #Init sounds
    selected_music2, selected_music3 = init_sound()

    while True:

        if ev_read_line.is_set():
            if once_read_line == False:
                invert = False
                once_read_line = True
                flag_forward = 0
                flag_left = 0
                flag_right = 0
                state = 0
                count_bl = 0
                usb.write(b"MT0 MC MD1 RI160 AT100 DT100 V10")
                pygame.mixer.music.load(selected_music2)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pass

            # LINE SENSOR READING
            read_serial_th.set()
            usb.write(b"SL")            # Send command to read line sensor
            sleep(0.01)                 # Wait to return datas
            data_line = commands_queue.get()      # Read data
            #print(f"dataline:{data_line}")


            if data_line[0] == 83 and data_line[1] == 76:     # Check if it is "S" e "L"
                left_sensor = data_line[4]
                central_sensor = data_line[10]
                right_sensor = data_line[16]

                print(f"Left: {left_sensor} - Central: {central_sensor} - Right: {right_sensor}")
                
                # Check if central sensor is reading black line or if all sensors are reading black
                if(((left_sensor == white) and (central_sensor == black) and (right_sensor == white)) or ((left_sensor == black) and (central_sensor == black) and (right_sensor == black))):
                    if(flag_forward == 0):
                        flag_forward = 1
                        flag_left = 0
                        flag_right = 0
                        count_bl = 0
                        usb.write(b"LT E1 RD20 GR70 BL30")
                        usb.write(b"MT0 MF")    # Moving to forward
                        sleep(0.1)# Wait to return datas

                # Check if only left sensor is reading black or left and central sensor is reading black
                elif((left_sensor == black) and (central_sensor == white) and (right_sensor == white)) or ((left_sensor == black) and (central_sensor == black) and (right_sensor == white)):
                    if(flag_left == 0):
                        flag_forward = 0
                        flag_left = 1
                        flag_right = 0
                        count_bl = 0
                        usb.write(b"MT0 ML")        # Turn left
                        usb.write(b"LT E1 RD0 GR0 BL50")
                        print("send left")
                        sleep(0.1)
                        

                # Check if only right sensor is reading black or central and right sensor is reading black
                elif((left_sensor == white) and (central_sensor == white) and (right_sensor == black)) or ((left_sensor == white) and (central_sensor == black) and (right_sensor == black)):
                    if(flag_right == 0):
                        flag_forward = 0
                        flag_left = 0
                        flag_right = 1
                        count_bl = 0
                        usb.write(b"MT0 MR")        # Turn right
                        usb.write(b"LT E1 RD0 GR50 BL00")
                        print("send rigth")
                        sleep(0.1)
                

                    # Check if all sensor is reading white
                elif((left_sensor == white) and (central_sensor == white) and (right_sensor == white)):
                    flag_forward = 0
                    count_bl += 1
                    usb.write(b"LT E1 RD50 GR0 BL0")
                    usb.write(b"MT0 MB")        # Moving to back
                    sleep(0.5)

                if count_bl >= 5:
                    ev_read_line.clear()
                    usb.write(b"MT0 MP")                # Moviment Pause
                    usb.write(b"MT0 ME0")               # Disables wheel motors on mode continuous

                 
           
            # DIGITAL INPUT READING
            read_serial_th.set()
            usb.write(b"DI0")
            sleep(0.01)   
            data_di = commands_queue.get()  # Read data
            #print(f"data_di:{data_di}")

            
            if data_di[6] == 68 and data_di[7] == 73:     # Check if it is "D" e "I"
                if data_di[10]==black:
                    flag_forward = 0
                    flag_left = 0
                    flag_right = 0
                    
                    sleep(0.2)   

                    if state == 0:
                        print("EXECUTING SECTION 1")
                        state = 1
                        usb.write(b"MT0 MP")
                        usb.write(b"MT0 D25 AT200 DT200 V10")
                        
                        if(invert):
                            usb.write(b"MT0 D89 R AT200 DT200 V10")
                        else:
                            usb.write(b"MT0 D89 L AT200 DT200 V10")
                        
                        usb.write(b"MT0 D300 AT200 DT200 V10")
                        
                        dType.SetHOMECmd(api_arm, temp = 0, isQueued = 1)       # Command to go to home position
                        
                        WaitSobot(wait, usb, read_serial_th)


                        x_arm, y_arm, _ = get_arm_coord_from_camera()

                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, x_arm, y_arm, 150, 0, isQueued = 1)[0]
                        MagicianIndex = dType.SetEndEffectorSuctionCup(api_arm, True,  True, isQueued=1)
                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, x_arm, y_arm, 55, 0, isQueued = 1)[0]
                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, x_arm, y_arm, 150, 0, isQueued = 1)[0]


                        while MagicianIndex > dType.GetQueuedCmdCurrentIndex(api_arm)[0]:
                            sleep(0.25)
                
                        
                        usb.write(b"MT0 D-300 AT200 DT200 V10")
                        if(invert):
                            usb.write(b"MT0 D89 L AT200 DT200 V10")
                        else:
                            usb.write(b"MT0 D91 R AT200 DT200 V10")
                        usb.write(b"MT0 D30 AT200 DT200 V10")

                        dType.dSleep(1000)
                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, 195, 0, 44, 0, isQueued = 1)[0]
                        
                        WaitSobot(wait, usb, read_serial_th)
                        



                    elif state == 1:
                        print("EXECUTING SECTION 2")
                        state = 2

                        usb.write(b"MT0 MP")
                        usb.write(b"MT0 D10 AT200 DT200 V10")

                        if(invert):
                            usb.write(b"MT0 D89 R AT200 DT200 V10")
                        else:
                            usb.write(b"MT0 D89 L AT200 DT200 V10")

                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, 275, -15, 90, 0, isQueued = 1)[0]
                        usb.write(b"MT0 D300 AT200 DT200 V10")
                        WaitSobot(wait, usb, read_serial_th)
                        
                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, 275, -15, 55, 0, isQueued = 1)[0]
                        MagicianIndex = dType.SetEndEffectorSuctionCup(api_arm, False,  False, isQueued=1)[0]
                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, 275, -15, 150, 0, isQueued = 1)[0]
                        
                        while MagicianIndex > dType.GetQueuedCmdCurrentIndex(api_arm)[0]:
                            sleep(0.25)

                
                        usb.write(b"MT0 D-300 AT200 DT200 V10")
                        if(invert):
                            usb.write(b"MT0 D89 L AT200 DT200 V10")
                        else:
                            usb.write(b"MT0 D89 R AT200 DT200 V10")
                        usb.write(b"MT0 D30 AT200 DT200 V10")

                        dType.dSleep(1000)
                        MagicianIndex = dType.SetPTPCmd(api_arm, 2, 195, 0, 44, 0, isQueued = 1)[0]

                        WaitSobot(wait, usb, read_serial_th)


                    
                    elif state == 2:
                        print("EXECUTING SECTION 3")
                        
                        state=0
                        
                        usb.write(b"MT0 MP")
                        invert = not invert
                        if(invert):
                            usb.write(b"MT0 D180 L AT200 DT200 V10")
                        else:
                            usb.write(b"MT0 D183 R AT200 DT200 V10")
                        
                        times_exec += 1
                        print(f"Exec {times_exec} times")
                        WaitSobot(wait, usb, read_serial_th)



                            

        else:
                if once_read_line == True:
                    once_read_line = False
                    pygame.mixer.music.load(selected_music3)
                    pygame.mixer.music.play()
                    stop_read_line(usb)
                    while pygame.mixer.music.get_busy():
                        pass