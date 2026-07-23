# Solis Robot - SoBot
![](imgs/SoBotArm.png)
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
* Robotic Arm - Dobot Magician Lite
* Wireless Gamepad F710  <img align="center" height="40" width="40" src="imgs\control.png">


# Programming Example
## [SMART MANIPULATION.py](Smart_Manipulation.py) 
This code implements a remote control system for the SoBot, using a Logitech controller to perform functions such as movement, speed adjustment, and LED color changes. Communication with the robot is established through a serial interface, enabling the exchange of commands and real-time responses. In addition to manual control, the program integrates line sensors that allow the SoBot to autonomously follow tracks, and upon detecting ground markers, it can perform object manipulation tasks supported by computer vision.

### Code Description
```
📂Smart Manipulation
     📂 aux_code               →  Helpers to detect color and arm pose
     📂 lib_arm                →  Libs needed from arm.
     📂 imgs                   →  Images for the repo.
     📂 sounds                 →  Sound assets for tasks.
     📘 Smart_Manipulation.py  →  Main Code ✅
     📘 aux_functions.py       →  Auxiliary Funcitions. 
     📘 read_gamepead.py       →  Functions to read gamepad.
     📘 read_line.py           →  Functions to read line.
````
This project uses threading to run multiple tasks in parallel (gamepad input, line sensing, and control loops). For clarity and maintainability, the logic is split across focused modules:

**Smart_Manipulation.py:** Initializes the system, starts worker threads, configures serial communication and movement parameters.

**read_gamepad.py:** Reads inputs from the Logitech controller and maps buttons/axes to robot actions: enabling/disabling motors, movement commands (forward/backward/left/right), curve modes, speed presets, and LED color changes.

**read_line.py:** Implements line-following behavior based on line sensor data. The robot adjusts its direction (left/right corrections, forward motion) to stay on track. When section points are detected by the edge sensors, object manipulation routines integrated into the vision pipeline are triggered.


# Reference Link
[SolisTecnologia website](https://www.solistecnologia.com.br/sobot)

# Please Contact Us
If you have any problem when using our robot after checking this tutorial, please contact us.

### Phone:
+55 1143040786

### Technical support email: 
contato@solistecnologia.com.br


![](imgs/logo.png)


