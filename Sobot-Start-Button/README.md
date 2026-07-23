# Solis Robot - SoBot
![](imgs/SoBotSingleLF.png)
# Introduction

AMR (autonomous mobile robotics) platform equipped with a camera system, ultrasonic and photoelectric sensors, works with a high rate of precision and repeatability of its movements, as it uses stepper motors in its movement and navigation, the SoBot also can be termed as a research and development interface, as it facilitates the practical experimentation of algorithms from the simplest to the most complex level.

This product was developed 100% by Solis Tecnologia, and has a lot of technology employing cutting-edge concepts, such as:

The motors can be controlled simultaneously or individually.
The user can select different accessories to implement to the robot.
Several programming languages can be used to connect via API.

# Components

* Main structure in aluminum
* Robot Control Driver
* Raspberry Pi 5B board <img align="center" height="30" width="40" src="https://github.com/devicons/devicon/blob/master/icons/raspberrypi/raspberrypi-original.svg">
* 2x NEMA-23 Stepper Motors
* 2x 12V/5A battery



# Programming Example
## [Start_Button.py](Start_Button.py) 
This code implements a push-button control system for the SoBot, allowing users to start and stop an external Python script using a single button connected to a Raspberry Pi. The first button press launches the external script, while the second press terminates it along with any child processes. The program uses GPIO for button input detection and includes debouncing to ensure reliable operation. It is designed for simplicity and robustness, making it ideal for initiating and managing tasks on the SoBot.

### Code Description
```
📂Start_Button
     📂 imgs                  →  Images for the repo.
     📘 Start_Button.py        → Main Code ✅
````
The program is contained in a single script, Start_Button.py, which handles the following: 

**GPIO Configuration:** Sets up pin 12 on the Raspberry Pi with a pull-down resistor for button input.

**Button Event Handling:** Detects button presses with a 1-second debounce, incrementing a counter to track presses. The first press starts the external script, and the second press terminates it.

**Process Management:** Uses the psutil library to gracefully terminate the external script and its child processes, ensuring clean shutdowns.

**Main Loop:** Runs indefinitely with a low CPU footprint, waiting for button events.

# Reference Link
[SolisTecnologia website](https://www.solistecnologia.com.br/sobot)

# Please Contact Us
If you have any problem when using our robot after checking this tutorial, please contact us.

### Phone:
+55 1143040786

### Technical support email: 
contato@solistecnologia.com.br


![](imgs/logo.png)

