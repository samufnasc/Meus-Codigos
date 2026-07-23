#!/usr/bin/python3
"""
Solis Robot - SoBot

Agri-Tech.py: Programming example for SoBot to perform tasks using the Agri-Tech module and computer vision for decision making.

Created By   : Vinicius M. Kawakami
Version      : 1.0

Company: Solis Tecnologia
"""

import serial               # Serial libary for USB communication
import cv2                  # Computer Vision Library OpenCV2
import numpy as np          # Numerical logic library
from time import time,sleep # System time library
from tracker import *       # Library developed to identify and track objects
import threading            # Library used to count timelines

'''
###################################
        Global Variables
###################################
'''

ContadorSaidas = 0              # Variable to count the green objects that passed through the detection zone
ContadorSaidasGreen = 0         # Variable to count the red objects that passed through the detection zone
AreaContornoLimiteMin = 30      # Minimum area value to detect contour
OffsetLinhaSaida = 60           # Value to position the output line
AreaCount = 10                  # Pixel value of the area to detect the contour
AreaMinY = 140                  # Determines the position of the line that starts detecting object
AreaMaxY = 310                  # Determines the position of the line that stops detecting objects
CoordenadaYLinhaSaida = 0       # Line coordinate that detects object
CoordenadaXLeft = 0             # Coordinate of the left vertical line that divides section 1 and 2
CoordenadaXCenter = 0           # Coordinate of the central vertical line that divides section 2 and 3
CoordenadaXRight = 0            # Coordinate of the right vertical line that divides section 3 and 4
ContadorQuad1 = 0               # Variable for counting VM objects in section 1
ContadorQuad2 = 0               # Variable for counting VM objects from section 2
ContadorQuad3 = 0               # Variable for counting VM objects from section 3
ContadorQuad4 = 0               # Variable for counting VM objects from section 4
idTempQ1 = 65535                # Variable to store a detected ID and count only once in section 1
idTempQ2 = 65535                # Variable to store a detected ID and count only once in section 2
idTempQ3 = 65535                # Variable to store a detected ID and count only once in section 3
idTempQ4 = 65535                # Variable to store a detected ID and count only once in section 4
count_p = 0                     # Incremental variable to identify start and end time triggers
flag_D1 = 0
flag_D2 = 0
flag_D3 = 0
flag_D4 = 0
'''
###################################
        Auxiliary Functions
###################################
'''
    
# Function to check if the object is passing in quadrant 1 of the monitored output line
def TestaQuad1(idQ1,y, c_y_out):
    global idTempQ1

    DiferencaAbsoluta = abs(y - c_y_out)
    if(DiferencaAbsoluta <= AreaCount):
        if idQ1 != idTempQ1:
            idTempQ1 = idQ1
            return 1
        else:
            return 0
    else:
        return 0

# Function to check if the object is passing in quadrant 2 of the monitored output line
def TestaQuad2(idQ2,y, c_y_out):
    global idTempQ2
    DiferencaAbsoluta = abs(y - c_y_out)
    if (DiferencaAbsoluta <= AreaCount):
        if idQ2 != idTempQ2:
            idTempQ2 = idQ2
            return 1
        else:
            return 0
    else:
        return 0

# Function to check if the object is passing in quadrant 3 of the monitored output line
def TestaQuad3(idQ3,y, c_y_out):
    global idTempQ3
    DiferencaAbsoluta = abs(y - c_y_out)
    if(DiferencaAbsoluta <= AreaCount):
        if(idQ3 != idTempQ3):
            idTempQ3 = idQ3
            return 1
        else:
            return 0
    else:
        return 0

# Function to check if the object is passing in quadrant 4 of the monitored output line
def TestaQuad4(idQ4,y,c_y_out):
    global idTempQ4
    DiferencaAbsoluta = abs(y - c_y_out)
    if(DiferencaAbsoluta <= AreaCount):
        if(idQ4 != idTempQ4):
            idTempQ4 = idQ4
            return 1
        else:
            return 0
    else:
        return 0

# Function of the threading.timer module with command arguments, serial configuration and status for sending a serial command
def TimerP (*args):
    cmd = args[0]
    serialUSB = args[1]
    print("Count_F"+str(args[3])+" "+str(args[2])+" "+str(cmd)+" "+str(time()))
    serialUSB.write(bytes(cmd, 'utf-8'))

# Function to mark the contours, check positioning, perform counting and start command trigger time for the robot
def CntsOutputTest(Frame,x, y, w, h, idOut,colorId,CoordYSaida,CoordXLeft,CoordXCenter,CoordXRight,serialUSB,width):
    global ContadorSaidas
    global ContadorSaidasGreen
    global ContadorQuad1
    global ContadorQuad2
    global ContadorQuad3
    global ContadorQuad4
    global count_p

    # Checks the color of the detected object and makes a rectangle around it
    if colorId:      # Check if it's red
        colorRet = (40,180,255)
    else:
        colorRet = (255,180,20)

    cv2.rectangle(Frame, (x, y), (x + w, y + h), colorRet, 2)

    # Determines the center point of the contour and draws a circle to indicate
    CoordenadaXCentroContorno = int((x+x+w)/2)
    CoordenadaYCentroContorno = int((y+y+h)/2)
    PontoCentralContorno = (CoordenadaXCentroContorno,CoordenadaYCentroContorno)
    cv2.circle(Frame, PontoCentralContorno, 1, (0, 0, 0), 1)

    # Tests intersection of contour centers with the reference line and its quadrants
    if (CoordenadaXCentroContorno >= 0) and (CoordenadaXCentroContorno <= CoordXLeft):
        if (TestaQuad1(idOut,CoordenadaYCentroContorno, CoordYSaida)):
            if colorId:
                count_p +=1
                ContadorQuad1 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P1 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO1 E1 TM400",serialUSB,"P1",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                
    if (CoordenadaXCentroContorno >= CoordXLeft+1) and (CoordenadaXCentroContorno <= CoordXCenter):
        if (TestaQuad2(idOut,CoordenadaYCentroContorno, CoordYSaida)):
            if colorId:
                count_p +=1
                ContadorQuad2 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P2 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO2 E1 TM400",serialUSB,"P2",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                
    if (CoordenadaXCentroContorno >= CoordXCenter+1) and (CoordenadaXCentroContorno <= CoordXRight):
        if (TestaQuad3(idOut,CoordenadaYCentroContorno,CoordYSaida)):
            if colorId:
                count_p +=1
                ContadorQuad3 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P3 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO3 E1 TM400",serialUSB,"P3",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                
    if (CoordenadaXCentroContorno >= CoordXRight+1) and (CoordenadaXCentroContorno <= width):
        if (TestaQuad4(idOut,CoordenadaYCentroContorno,CoordYSaida)):
            if colorId:
                count_p +=1 
                ContadorQuad4 += 1
                ContadorSaidas += 1
                print("Count_ST"+str(count_p)+" P4 timer: "+str(time()))
                threading.Timer(14.3, TimerP, args = ("DO4 E1 TM400",serialUSB,"P4",count_p)).start()
            else:
                ContadorSaidasGreen += 1
                


'''
###################################
        Main Functions
###################################
'''

# Set serial port
serialUSB = serial.Serial('/dev/ttyACM0', 57600, timeout=0, dsrdtr=False)
serialUSB.flush()       # Waits data configuration

# Configure wheel parameters
serialUSB.write(b"WP MT1 WD99,65")
serialUSB.write(b"WP MT2 WD100,25")
serialUSB.write(b"WP DW261")
sleep(0.1)

camera = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Capture video from camera

# Set camera settings
camera.set(3, 640)  # set frame width
camera.set(4, 360)  # set frame height
camera.set(5, 15)   # set frame rate
camera.set(cv2.CAP_PROP_BRIGHTNESS, 128)
camera.set(cv2.CAP_PROP_CONTRAST, 32)
camera.set(cv2.CAP_PROP_AUTO_WB, 1)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

kernel = np.ones((3, 3), np.uint8)

###### DARK GREEN #####
#lower = np.array([70, 100, 100])
#upper = np.array([77, 200, 200])
###### LIGHT GREEN #####
#lower = np.array([44, 100, 120])
#upper = np.array([55, 200, 220])
###### LIGHT GREEN WITH WHITE BACKGROUND #####
green_lower = np.array([44, 85, 50])
green_upper = np.array([55, 230, 160])
##### RED #####
#lower2 = np.array([0, 85, 150])
#upper2 = np.array([15, 255, 255])
##### RED WITH WHITE BACKGROUND #####
red_lower1 = np.array([0, 115, 80])
red_upper1 = np.array([10, 230, 185])
red_lower2 = np.array([170, 115, 80])
red_upper2 = np.array([180, 230, 185])
##### PURPLE WITH WHITE BACKGROUND #####
#lower3 = np.array([120, 75, 80])
#upper3 = np.array([140, 220, 185])


# Initialize tracking variables
tracker = EuclideanDistTracker()

#Loop to read some frames before starting the analysis to stabilize the camera's brightness
for i in range(0,20):
    grabbed, Frame = camera.read()


while True:
    # Reads the frames of the image
    (grabbed, Frame) = camera.read()

    # Check if it was possible to obtain frame
    if not grabbed:
        break
    
    # Determines the height and width of the frame
    height = int(np.size(Frame,0))
    width = int(np.size(Frame,1))

    CoordenadaYLinhaSaida = int((height / 2)+OffsetLinhaSaida)
    CoordenadaXLeft = int(((width/2)/2)-1)
    CoordenadaXCenter = int(width/2)
    CoordenadaXRight = int((width/2) + CoordenadaXLeft + 2)

    # Determines the region to perform object identification
    roi = Frame[AreaMinY:AreaMaxY, 0:width]

    # Filters for frame color treatment
    FrameBulr = cv2.GaussianBlur(roi, (19, 19), 0)
    FrameHsv = cv2.cvtColor(FrameBulr, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), np.uint8)
    erode = cv2.erode(FrameHsv, kernel, iterations=1)
    dilate = cv2.dilate(erode, kernel, iterations=1)

    # Determines the Color Range for locating contours
    Range1 = cv2.inRange(dilate, green_lower, green_upper)
    Range2 = cv2.inRange(dilate, red_lower1, red_upper1)
    Range3 = cv2.inRange(dilate, red_lower2, red_upper2)
    Range = Range1 + Range2 + Range3
    
    cnts,_ = cv2.findContours(Range.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Scans the areas found
    detections = []

    for c in cnts:
        # contours of very small area are ignored
        #print(str(cv2.contourArea(c))+' '+str(color))
        if cv2.contourArea(c) > AreaContornoLimiteMin: 
            # get contour coordinates and highlight the contour with a rectangle
            (x, y, w, h) = cv2.boundingRect(c)  #x e y: top left vertex coordinates
                                                #w e h: respectively width and height of the rectangle
            # Adds found contour to tracking function
            detections.append([x, y, w, h])


    # Marks the traced contours on the screen and counts them
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        colorHSV = []
        x, y, w, h, id = box_id
        colorHSV = dilate[int(y+(h/2))][int(x+(w/2))]
        if (colorHSV[0] >= red_lower1[0] and colorHSV[0] <= red_upper1[0]) or (colorHSV[0] >= red_lower2[0] and colorHSV[0] <= red_upper2[0]):
            colorId = 1
        elif colorHSV[0] >= green_lower[0] and colorHSV[0] <= green_upper[0]:
            colorId = 0
        
        CntsOutputTest(Frame, x, y+AreaMinY, w, h, id, colorId, CoordenadaYLinhaSaida, CoordenadaXLeft, CoordenadaXCenter, CoordenadaXRight,serialUSB,width)

    # Informs in the image the number of objects that passed through the predetermined zones
    TotalSaidas = ContadorSaidasGreen + ContadorSaidas

    # Draw reference lines
    cv2.line(Frame, (CoordenadaXLeft,0), (CoordenadaXLeft,height), (200, 255, 100), 1)
    cv2.line(Frame, (CoordenadaXCenter,0), (CoordenadaXCenter,height), (200, 255, 100), 1)
    cv2.line(Frame, (CoordenadaXRight,0), (CoordenadaXRight,height), (200, 255, 100), 1)
    cv2.line(Frame, (0,CoordenadaYLinhaSaida), (width,CoordenadaYLinhaSaida), (0, 0, 200), 6)
    cv2.line(Frame, (0,AreaMinY), (width,AreaMinY), (200, 255, 100), 1)
    cv2.line(Frame, (0,AreaMaxY), (width,AreaMaxY), (200, 255, 100), 1)

    cv2.rectangle(Frame, (0,0), (width,27), (255,255,255), -1)
    cv2.rectangle(Frame, (0,height-25), (width,height), (255,255,255), -1)

    cv2.putText(Frame, "BOM: {}".format(str(ContadorSaidasGreen)), (10, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, (0, 165, 0), 2)
    cv2.putText(Frame, "RUIM: {}".format(str(ContadorSaidas)), (243, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, (0, 0, 200), 2)
    cv2.putText(Frame, "TOTAL: {}".format(str(TotalSaidas)), (436, 20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, (220, 100, 0), 2)
    cv2.putText(Frame, "SE1: {}".format(str(ContadorQuad1)), (3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)
    cv2.putText(Frame, "SE2: {}".format(str(ContadorQuad2)), (CoordenadaXLeft + 3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)
    cv2.putText(Frame, "SE3: {}".format(str(ContadorQuad3)), (CoordenadaXCenter + 3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)
    cv2.putText(Frame, "SE4: {}".format(str(ContadorQuad4)), (CoordenadaXRight + 3, height - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 220), 1)

    # Show the frame image
    cv2.imshow("Original", Frame)

    # checks if any button was pressed
    buttonKey = cv2.waitKey(1)

    if buttonKey == ord('q'):   # If button 'q', ends the application 
        break

    if buttonKey == ord('f'):   # If button 'f', move forward
        serialUSB.write(b"LT E1 RD20 GR70 BL30")
        serialUSB.write(b"MT0 E1 D1000 AT300 DT300 V8")   


    if buttonKey == ord('b'):   # If button 'b', break the movement
        serialUSB.write(b"MT0 BC")
        serialUSB.write(b"MT0 E0")
        serialUSB.write(b"LT E0 RD0 GR0 BL0") 

    if buttonKey == ord('s'):   # If button 's', enable the motors
        serialUSB.write(b"MT0 E1")
        serialUSB.write(b"LT E1 RD20 GR70 BL30") 
    
    if buttonKey == ord('1'):   # If button '1', controls digital output 1
        if flag_D1 == 0:
            flag_D1 = 1
            serialUSB.write(b"DO1 E1")
        else:
            flag_D1 = 0
            serialUSB.write(b"DO1 E0")

    if buttonKey == ord('2'):   # If button '2', controls digital output 2
        if flag_D2 == 0:
            flag_D2 = 1
            serialUSB.write(b"DO2 E1")
        else:
            flag_D2 = 0
            serialUSB.write(b"DO2 E0")

    if buttonKey == ord('3'):   # If button '3', controls digital output 3
        if flag_D3 == 0:
            flag_D3 = 1
            serialUSB.write(b"DO3 E1")
        else:
            flag_D3 = 0
            serialUSB.write(b"DO3 E0")

    if buttonKey == ord('4'):   # If button '4', controls digital output 4
        if flag_D4 == 0:
            flag_D4 = 1
            serialUSB.write(b"DO4 E1")
        else:
            flag_D4 = 0
            serialUSB.write(b"DO4 E0")


# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


# Let CTRL+C actually exit