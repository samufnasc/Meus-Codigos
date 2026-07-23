
#!/usr/bin/python3
"""
Solis Robot - SoBot

Start_Button.py: Programming example to initialize another program using the push button present in the SoBot

Created By   : Rodrigo L. de Carvalho
Version      : 1.0

Company: Solis Tecnologia
"""


import RPi.GPIO as GPIO
from time import sleep
import subprocess
import psutil

# Set up GPIO using physical pin numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Configure pin 12 with pull-down resistor

# Global variables
press_count = 0
external_process = None

def terminate_process_and_children(pid):
    """Terminate a process and all its child processes."""
    try:
        # Get the main process
        parent = psutil.Process(pid)
        # Get all child processes
        children = parent.children(recursive=True)
        
        # Send SIGTERM to child processes
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        
        # Send SIGTERM to the main process
        parent.terminate()
        
        # Wait for processes to terminate gracefully
        gone, still_alive = psutil.wait_procs(children + [parent], timeout=3)
        
        # Forcefully kill any remaining processes
        for proc in still_alive:
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                pass
                
    except psutil.NoSuchProcess:
        print("Process already terminated or does not exist.")
    except Exception as e:
        print(f"Error terminating processes: {e}")

def button_callback(channel):
    """Handle button press events."""
    global press_count, external_process

    press_count += 1

    if press_count == 1:
        print("First press: Starting external script...")
        external_process = subprocess.Popen(["python3", "/home/pi/Documentos/Projetos/Demo/Start_prog/Start_prog_SL.py"]) #MODIFY
    
    
    elif press_count == 2:
        print("Second press: Terminating everything...")
        
        # Terminate the external process if it's still running
        if external_process and external_process.poll() is None:
            terminate_process_and_children(external_process.pid)
        
        press_count = 0

# Set up button event detection with debounce
GPIO.add_event_detect(12, GPIO.RISING, callback=button_callback, bouncetime=1000)
print("Waiting for button press... (First press starts, second press stops)")

# Main loop to keep the program running
while True:
    sleep(0.1)  # Prevent CPU overload