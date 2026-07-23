# SoBot-Agri-Tech
 Programming example for SoBot to perform tasks using the Agri-Tech module and computer vision for decision making.


# Solis Robot - SoBot
![](https://github.com/SolisTecnologia/SoBot-Agri-Tech/blob/main/png/SoBotAgro.png)
# Introduction

AMR (autonomous mobile robotics) platform equipped with a camera system, ultrasonic and photoelectric sensors, works with a high rate of precision and repeatability of its movements, as it uses stepper motors in its movement and navigation, the SoBot also can be termed as a research and development interface, as it facilitates the practical experimentation of algorithms from the simplest to the most complex level.

This product was developed 100% by Solis Tecnologia, and has a lot of technology employing cutting-edge concepts, such as:

The motors can be controlled simultaneously or individually.  
The user can select different accessories to implement to the robot.  
Several programming languages can be used to connect via API.  

# Components

* Main structure in aluminum
* Robot Control Driver
* Agri-Tech Module
* Camera Webcam
* Raspberry Pi 4B board <img align="center" height="30" width="40" src="https://github.com/devicons/devicon/blob/master/icons/raspberrypi/raspberrypi-original.svg">
* 2x NEMA-23 Stepper Motors
* 2x 12V/5A battery

# Programming Example

 Programming example for SoBot to perform tasks using the Agri-Tech module and computer vision for decision making.

The library used for computer vision is OpenCV. It contains several functions and algorithms to process images and videos, such as object detection, face recognition, object tracking, camera calibration, among other features.

The application of the computer vision technique is used in this example to detect objects with specific chromatic characteristics, such as green and red, which can be associated, respectively, with healthy and diseased plants. When carrying out this identification, the programming triggers the liquid release system directed only to the plants diagnosed as sick, making the liquid application system precise and efficient.

### Programming Language

* Python  <img align="center" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">


## Agri-Tech application - [Agri-Tech.py](https://github.com/SolisTecnologia/SoBot-Agri-Tech/blob/master/Agri-Tech.py)

### Required Libraries

~~~python
import serial
import cv2
import numpy as np
from time import time,sleep
from tracker import *
import threading
~~~
  
The ''serial'' library for serial/usb Raspberry connection with the robot controller driver.  
The ''cv2'' library is used to apply the computer vision technique.  
The "numpy" library is used with mathematical matrix functions.  
The ''time'' library is needed to generate time delays.  
The "tracker" library was developed to identify and track objects.  
The "threading" library is used to count timelines for triggering the liquid release system.  
  

### Code Description

#### SoBot Control Commands

The commands used to control the SoBot in this example are movement commands in fixed mode, commands to control the LED strip lighting and commands are also used to control the digital outputs to activate the liquid dispersion system of the Agri-Tech module.

~~~python
serialUSB.write(b"LT E1 RD20 GR70 BL30")
serialUSB.write(b"MT0 E1 D1200 AT1500 DT1500 V8")   # Initial straight

serialUSB.write(b"DO1 E1")	# Turn On digital output 1
serialUSB.write(b"DO1 E0")	# Turn Off digital output 1
serialUSB.write(b"DO2 E1")	# Turn On digital output 2
serialUSB.write(b"DO2 E0")	# Turn Off digital output 2
serialUSB.write(b"DO3 E1")	# Turn On digital output 3
serialUSB.write(b"DO3 E0")	# Turn Off digital output 3
serialUSB.write(b"DO4 E1")	# Turn On digital output 4
serialUSB.write(b"DO4 E0")	# Turn Off digital output 4
~~~

#### Functions and logic for Computer Vision

The **'VideoCapture'** function is used to read video frames and the **'read'** function returns an indication if the reading was successful and the frame captured.

~~~python
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
(grabbed, Frame) = camera.read()
~~~

To process the images, use the following functions:  
• The **'GussianBlur'** function smooths the image to improve edge detection.  
• The **'cvtColor'** function converts the image from BGR (Blue-Green-Red) color to HSV (Hue-Saturation-Value) color to make it easier to detect objects based on their color.  
• The **'erode'** function reduces the image with erosion process to remove unwanted small objects, separates objects and sharpens object boundaries.  
• The **'dilate'** function enlarges the image with dilation process.  

~~~python
# Filters for frame color treatment
FrameBulr = cv2.GaussianBlur(roi, (19, 19), 0)
FrameHsv = cv2.cvtColor(FrameBulr, cv2.COLOR_BGR2HSV)
erode = cv2.erode(FrameHsv, kernel, iterations=1)
dilate = cv2.dilate(erode, kernel, iterations=1)
~~~

To obtain an image color filter, variables that store arrays with predefined values for the red and green color ranges are used.

~~~python
###### LIGHT GREEN WITH WHITE BACKGROUND #####
lower = np.array([40, 50, 120])
upper = np.array([80, 100, 255])
##### RED WITH WHITE BACKGROUND #####
lower2 = np.array([0, 50, 80])
upper2 = np.array([10, 230, 255])
lower1 = np.array([170, 50, 80])
upper1 = np.array([180, 230, 255])
~~~

The **'inRange'** function creates a binary mask that keeps only the pixels of an image that are within the predefined color range in the lower and upper variables. The sum of all masks generates a range of colors that we want to keep in the image.
Next, the **'findContours'** function finds the contours of objects with predefined colors.

~~~python
# Determines the Color Range for locating contours
Range1 = cv2.inRange(dilate, lower, upper)
Range2 = cv2.inRange(dilate, lower2, upper2)
Range3 = cv2.inRange(dilate, lower1, upper1)
Range = Range1 + Range2 + Range3
cnts,_ = cv2.findContours(Range.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
~~~

Checks if the contour is greater than the established minimum value, highlights the found contours with a rectangle and adds them to the list of contours for the follow function.

~~~python
for c in cnts:
    # contours of very small area are ignored
    #print(str(cv2.contourArea(c))+' '+str(color))
    if cv2.contourArea(c) > AreaContornoLimiteMin: 
        # get contour coordinates and highlight the contour with a rectangle
        (x, y, w, h) = cv2.boundingRect(c)  #x e y: top left vertex coordinates
                                            #w e h: respectively width and height of the rectangle
        # Adds found contour to tracking function
        detections.append([x, y, w, h])
~~~

After identifying the objects, functions from the **'tracker'** library are used to number and follow the objects, then the **'CntsOutputTest'** function checks the position of each object on the screen to trigger the respective digital output.

~~~python
tracker = EuclideanDistTracker()

# Marks the traced contours on the screen and counts them
boxes_ids = tracker.update(detections)
for box_id in boxes_ids:
    colorHSV = []
    x, y, w, h, id = box_id
    colorHSV = dilate[int(y+(h/2))][int(x+(w/2))]
    if (colorHSV[0] >= 0 and colorHSV[0] <= 15) or (colorHSV[0] >= 170 and colorHSV[0] <= 180):
        #TextColor = "Red"
        colorId = 1
    elif colorHSV[0] >= 40 and colorHSV[0] <= 80:
        #TextColor = "Green"
        colorId = 0

    CntsOutputTest(Frame,x, y+AreaMinY, w, h, id,colorId,CoordenadaYLinhaSaida,CoordenadaXLeft,CoordenadaXCenter,CoordenadaXRight,serialUSB,width)
~~~


### Flowchart

![](https://github.com/SolisTecnologia/SoBot-Agri-Tech/blob/main/png/Flowchart_Agri-Tech.png)

## Agri-Tech application - [tracker.py](https://github.com/SolisTecnologia/SoBot-Agri-Tech/blob/main/tracker.py)

### Required Libraries

~~~python
import math
~~~

The ''math'' library is used to calculate trigonometric function

### Code Description

Finds the center of detected objects.

~~~python
# Get center point of new object
for rect in objects_rect:
    x, y, w, h = rect
    cx = (x + x + w) // 2
    cy = (y + y + h) // 2
~~~

Checks if the object has moved 25 pixels in either direction relative to the center of the object. If detected for the first time, it marks an ID to identify it, if the object already has an ID, it only obtains its position on the screen.


~~~python
# Find out if that object was detected already
same_object_detected = False
for id, pt in self.center_points.items():
    dist = math.hypot(cx - pt[0], cy - pt[1])

    if dist < 25:
        self.center_points[id] = (cx, cy)
       #print(self.center_points)
       objects_bbs_ids.append([x, y, w, h, id])
       same_object_detected = True
       break

    # New object is detected we assign the ID to that object
    if same_object_detected is False:
        self.center_points[self.id_count] = (cx, cy)
        objects_bbs_ids.append([x, y, w, h, self.id_count])
        self.id_count += 1
~~~
  
  

For more information about the commands used, check the Robot Commands Reference Guide.


# Reference Link
[SolisTecnologia website](https://www.solistecnologia.com.br/produtos/estacoes_sobot)

# Please Contact Us
If you have any problem when using our robot after checking this tutorial, please contact us.

### Phone:
+55 1143040786

### Technical support email: 
contato@solistecnologia.com.br

![](https://github.com/SolisTecnologia/SoBot-Simple-Route/blob/master/png/logo.png)
