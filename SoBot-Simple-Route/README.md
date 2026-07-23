# Solis Robot - SoBot
![](https://github.com/SolisTecnologia/SoBot-Simple-Route/blob/master/png/SoBotSingle.png)
# Introduction

AMR (autonomous mobile robotics) platform equipped with a camera system, ultrasonic and photoelectric sensors, works with a high rate of precision and repeatability of its movements, as it uses stepper motors in its movement and navigation, the SoBot also can be termed as a research and development interface, as it facilitates the practical experimentation of algorithms from the simplest to the most complex level.

This product was developed 100% by Solis Tecnologia, and has a lot of technology employing cutting-edge concepts, such as:

The motors can be controlled simultaneously or individually.
The user can select different accessories to implement to the robot.
Several programming languages can be used to connect via API.

# Components

* Main structure in aluminum
* Robot Control Driver
* Raspberry Pi 4B board <img align="center" height="30" width="40" src="https://github.com/devicons/devicon/blob/master/icons/raspberrypi/raspberrypi-original.svg">
* 2x NEMA-23 Stepper Motors
* 2x 12V/5A battery

# Programming Example
## Basic Control - [Simple-Route.py](https://github.com/SolisTecnologia/SoBot-Simple-Route/blob/master/Simple-Route.py)
Programming example for the SoBot to move a simple route.

In this example, the robot will move 1 meter forward, 90° to the right, 1 meter forward, 90° to the left and 1 meter forward to finish.

![](https://github.com/SolisTecnologia/SoBot-Simple-Route/blob/master/png/Simple-route-course.png)

### Programming Language

* Python  <img align="center" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">

### Required Libraries

~~~python
from time import sleep
import serial
~~~

The ''time'' library is needed to generate time delays and the ''serial'' library for serial/usb Raspberry connection with the robot controller driver.



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
