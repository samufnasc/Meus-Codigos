import serial
import serial.tools.list_ports
import pygame
import os
import lib_arm.DobotDllType as dType
import cv2
import numpy as np

'''
###################################
        Auxiliary Functions
###################################
'''

def get_arm_coord_from_camera():

    print("Starting camera")


    #Global Variables
    
    #Color HSV
    color_high = np.array([35, 255, 255])   # #Modify 
    color_low = np.array([17, 80, 177])   # Modify 
    
    #Reference coordinates in pixels 
    x_base = 267 # Modify 
    y_base = 243 # Modify 

    #Reference coordinates of Arm
    x_arm = 261 # Modify 
    y_arm = 4  # Modify 

    # Capture video from camera
    cap = cv2.VideoCapture(0,cv2.CAP_V4L2)
    
    # Set camera settings
    cap.set(3, 640)
    cap.set(4, 360)
    cap.set(cv2.CAP_PROP_FPS, 25) 
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 64) 
    cap.set(cv2.CAP_PROP_CONTRAST, 64) 
    cap.set(cv2.CAP_PROP_AUTO_WB, 1)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

    #Main Loop
    count = 0
    while count < 15:
        # Captures a video frame
        ret, frame = cap.read()
        
        # Checks if the frame was captured successfully
        if not ret:
            print("Error capturing video frame")
            break
        
        # Filtres
        FrameBulr = cv2.GaussianBlur(frame, (19, 19), 0)
        FrameHsv = cv2.cvtColor(FrameBulr, cv2.COLOR_BGR2HSV)
        kernel = np.ones((3, 3), np.uint8)
        erode = cv2.erode(FrameHsv, kernel, iterations=1)
        dilate = cv2.dilate(erode, kernel, iterations=1)
        
        #Mask
        range = cv2.inRange(dilate, color_low, color_high)
        
        # Remove noise
        mask = cv2.morphologyEx(range, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
        
        # Find Contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
                area = cv2.contourArea(cnt)
                print("Area: ", area)
                if area > 4000:   #Discard small noise

                    # Get square delimiter
                    rect = cv2.minAreaRect(cnt)  
                    box = cv2.boxPoints(rect)  
                    box = np.int0(box)

                    #Central Point
                    (x_cam_new, y_cam_new) = rect[0]
                    x_cam_new, y_cam_new = int(x_cam_new), int(y_cam_new)

                    (w, h) = rect[1] 

                    # Draw frame
                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                    cv2.circle(frame, (x_cam_new, y_cam_new), 5, (0, 0, 255), -1)
                    
                    # Convert
                    # 120px == 40mm
                    # 1px == 3mm
                    w_mm = w / (120/40)

                    cv2.putText(frame, str(round(w_mm,2)), (x_cam_new,y_cam_new),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

                    print(f"Count{count} - Pos X:{x_cam_new}  Pos Y:{y_cam_new}")
        
                    count+=1
        

        # Show Result
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

    print(f"Pos X: {x_cam_new}")
    print(f"Pos Y: {y_cam_new}")

    y_arm = y_arm - ((x_cam_new-x_base)/3)
    x_arm = x_arm -((y_cam_new-y_base)/3)

    print(f"Xarm:{x_arm} Yarm:{y_arm}")
    return x_arm, y_arm, frame

#Function to find the serial port that the SoBot board is connected to
def serial_device_finder (name_device):
    # List all available serial ports
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        # Check if the port description contains the device name
        if name_device in port.description:
            print(f"Device found: {port.device} - {port.description}")
            return port.device

    # If can't find the device
    print(f"Device '{name_device}' not found.")
    return None


#Function to always read serial from SOBOT
def Read_Serial(read_serial_th, usb, wait, commands_queue):
    while True:
        read_serial_th.wait()
        command = usb.readline() # Read data
        if(command != b''): 
            print("Command received",command) 
            read_serial_th.clear()

            if(command == b'CR OK DL\r\n'):
                    wait.set()
            else:
                commands_queue.put(command) # Sends data to the queue

def WaitSobot(wait, usb, read_serial_th):
    read_serial_th.set()
    usb.write(b"DL100")
    wait.wait()
    wait.clear()


def init_sound():
    pygame.mixer.init()
    start_sound = '/home/pi/Documentos/Projetos/Demo/Smart_Manipulation/sounds'
    selected_music1 = os.path.join(start_sound, 'Frase_Start-Sobot.mp3')
    selected_music2 = os.path.join(start_sound, 'SL_Ativado.mp3')
    selected_music3 = os.path.join(start_sound, 'SL_Desativado.mp3')
    pygame.mixer.music.load(selected_music1)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

    return selected_music2, selected_music3


def Connect_Dobot():
    Desc_Dobot_serial = "Virtual COM Port - Hiker sudio"
    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

    # Serial connection to the Magician Lite Arm
    usb_Dobot = [0]
    api = dType.load()
    serial_Dobot = serial_device_finder(Desc_Dobot_serial)

    if serial_Dobot:
        # Connect to the found device
        usb_Dobot = dType.ConnectDobot(api, serial_Dobot, 115200)[0]

        print("Connect Dobot status:",CON_STR[usb_Dobot])

    else:
        print("No Serial Dobot was connected.")

    if (usb_Dobot == dType.DobotConnect.DobotConnect_NoError):

        dType.SetQueuedCmdClear(api)

        dType.SetEndEffectorSuctionCup(api, False, True, isQueued=0)     # Disable Suction Command

        #Move settings
        dType.SetHOMEParams(api, 220, 0, 150, 0, isQueued = 1)                # Sets the default position of the Dobot Magicia
        dType.SetPTPJointParams(api, 80, 80, 80, 80, 80, 80, 80, 80, isQueued = 1)  # Sets the joint parameters
        dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)                       # Defines the velocity ratio and acceleration ratio in PTP mode
        dType.SetPTPCoordinateParams(api, 200, 200, 400, 200, isQueued = 1)         # Set the velocity and acceleration of the Cartesian coordinate axis en PTP mode
                                                                                    # (api, xyzVelocity, rVelocity, xyzAcceleration, rAcceleration, isQueued)

        dType.SetHOMECmd(api, temp = 0, isQueued = 1)       # Command to go to home position

        return api
    


