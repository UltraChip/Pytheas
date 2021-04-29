## PYTHEAS CONTROL SYSTEM
##
## Primary control interface for the Pytheas
## Underwater Sensor Platform (USP).

from prettytable import PrettyTable
from time import strftime, sleep, time
import os, subprocess, sys
import logging
import io
import picamera
import threading
import socket
import math
import csv
import RPi.GPIO as gpio


# Quick Values: Settings you might need to change quickly

fileroot = "./"      # Root file path where data gets saved
logfile = "pcs.log"  # Location of the PCS log file
camrot = 0           # Default rotation for the camera


# Function declarations
def dummy(func_name):
    # Provides dummy output (and a log message) for functions that aren't fully developed yet
    #logging.debug(func_name + " was called.")
    return 10

def header():
    # Prints header
    os.system('clear')
    print ("+------------------------------------------------------------------------------------+")
    print ("|                               PYTHEAS CONTROL SYSTEM                               |")

def subheader(menuname):
    # Prints the header for submenus
    titlelen = 84
    leftpadlen = math.floor((titlelen - len(menuname))/2)
    rightpadlen = math.ceil((titlelen - len(menuname))/2)
    titleline = "|" + " "*leftpadlen + menuname + " "*rightpadlen + "|"
    hborder = "+------------------------------------------------------------------------------------+"

    header()
    print(hborder)
    print(titleline)
    print(hborder)
    print()

def refreshUI():
    # Prints the main menu & adds entry to the passive capture log
    headertable.clear_rows()
    ltime, pressure, depth, etemp, itemp = writeLog("")
    headertable.add_row([ltime, str(pressure) + " mbar", str(depth) + " m", str(etemp) + " C", str(itemp) + " C"])
    
    if gpio.input(lamp):
        lampStatus = "ON"
    else:
        lampStatus = "OFF"
    if isAcap():
        acapStatus = "ACTIVE"
    else:
        acapStatus = "inactive"

    header()
    print (headertable)
    print ()
    print ("Streaming video at tcp/h264://192.168.1.2:19212")
    print ("ACAP is currently {}.".format(acapStatus))
    print ()
    print ("1. Capture Picture")
    print ("2. Automatic Data Capture")
    print ("3. Change Camera Settings")
    print ("4. Write Note to Log")
    print ("5. Toggle Lamp (Currently {})".format(lampStatus))
    print ("-----")
    print ("9. Refresh Display")
    print ("0. Quit MCD")
    print ()

def getReadings():
    # Polls the sensors & gathers data
    ltime = strftime("%H:%M:%S")
    pressure = dummy("getReadings-pressure")
    depth = dummy("getReadings-depth")
    etemp = dummy("getReadings-etemp")
    itemp = round(float(subprocess.getoutput('cat /sys/class/thermal/thermal_zone0/temp')) / 1000, 2)
    return ltime, pressure, depth, etemp, itemp

def writeLog(note):
    ltime, pressure, depth, etemp, itemp = getReadings()
    with open(sessionFullFile, mode='a') as file:
        dx = csv.writer(file)
        dx.writerow([ltime, pressure, depth, etemp, itemp, note])
    return ltime, pressure, depth, etemp, itemp

def capture(capmode):
    # Captures a single picture
    lampstatus = gpio.input(lamp)
    gpio.output(lamp, flash)
    try:
        cam.resolution = (3280, 2464)  # 3280x2462 == max resolution of picamera v2
    except picamera.exc.PiCameraRuntimeError:
        logging.info("Preview stream is open - camera capturing at reduced resolution.")
    filename = "{}_{}_{}.png".format(sessionName, capmode, strftime("%Y%m%d-%H%M%S"))
    buildAnnotate()
    cam.capture("{}/{}".format(sessionPath, filename))
    logging.info("Picture captured as "+ filename)
    gpio.output(lamp, lampstatus)
    return filename

def camsettings():
    # Allows adjustment of the camera settings
    def setbrightness():
        print()
        print("Camera brightness can be any integer from 0 to 100.")
        print("It is currently {}. The default is 50.".format(cam.brightness))
        print()
        choice = int(input("What do you want to set the brightness to? "))
        if not choice:
            return
        if choice < 0:
            choice = 0
        if choice > 100:
            choice = 100
        cam.brightness = choice
        return

    def setcontrast():
        print()
        print("Camera contrast can be any integer from -100 to 100.")
        print("It is currently {}. The default is 0.".format(cam.contrast))
        print()
        choice = int(input("What do you want to set the contrast to? "))
        if not choice:
            return
        if choice < -100:
            choice = -100
        if choice > 100:
            choice = 100
        cam.contrast = choice
        return
    
    def setexposure():
        print()
        print("Camera exposure can be any of the following:")
        print("1. auto")
        print("2. night")
        print("3. nightpreview")
        print("4. backlight")
        print("5. spotlight")
        print("6. sports")
        print("7. snow")
        print("8. beach")
        print("9. fixedfps")
        print("10. antishake")
        print("11. fireworks")
        print()
        print("It is currently {}. The default is auto".format(cam.exposure_mode))
        print()
        choice = int(input("What do you want to set the exposure mode to? "))
        if not choice:
            return
        if choice < 1 or choice > 11:
            return
        if choice == 1:
            cam.exposure_mode = 'auto'
        elif choice == 2:
            cam.exposure_mode = 'night'
        elif choice == 3:
            cam.exposure_mode = 'nightpreview'
        elif choice == 4:
            cam.exposure_mode = 'backlight'
        elif choice == 5:
            cam.exposure_mode = 'spotlight'
        elif choice == 6:
            cam.exposure_mode = 'sports'
        elif choice == 7:
            cam.exposure_mode = 'snow'
        elif choice == 8:
            cam.exposure_mode = 'beach'
        elif choice == 9:
            cam.exposure_mode = 'fixedfps'
        elif choice == 10:
            cam.exposure_mode = 'antishake'
        elif choice == 11:
            cam.exposure_mode = 'fireworks'
        return

    def setwb():
        print()
        print("Camera white balance can be any of the following:")
        print("1. auto")
        print("2. sunlight")
        print("3. cloudy")
        print("4. shade")
        print("5. tungsten")
        print("6. fluorescent")
        print("7. incandescent")
        print("8. flash")
        print("9. horizon")
        print()
        print("It is currently {}. The default is auto".format(cam.awb_mode))
        print()
        choice = int(input("What do you want to set the exposure mode to? "))
        if not choice:
            return
        if choice < 1 or choice > 9:
            return
        if choice == 1:
            cam.awb_mode = 'auto'
        elif choice == 2:
            cam.awb_mode = 'sunlight'
        elif choice == 3:
            cam.awb_mode = 'cloudy'
        elif choice == 4:
            cam.awb_mode = 'shade'
        elif choice == 5:
            cam.awb_mode = 'tungsten'
        elif choice == 6:
            cam.awb_mode = 'fluorescent'
        elif choice == 7:
            cam.awb_mode = 'incandescent'
        elif choice == 8:
            cam.awb_mode = 'flash'
        elif choice == 9:
            cam.awb_mode = 'horizon'
        return

    global flash
    while True:
        if flash:
            flashStatus = "ON"
        else:
            flashStatus = "OFF"
        subheader("Adjust Camera Settings")

        print ("1. Brightness (currently {})".format(cam.brightness))
        print ("2. Contrast (currently {})".format(cam.contrast))
        print ("3. Exposure Mode (currently {})".format(cam.exposure_mode))
        print ("4. White Balance Mode (currently {})".format(cam.awb_mode))
        print ("5. Use Lamp During Capture (currently {})".format(flashStatus))
        print ("-----")
        print ("9. Reset everything to defaults")
        print ("0. Go back to main menu")
        print()
        choice = int(input("Please choose a command: "))

        if choice == 1:
            setbrightness()
        elif choice == 2:
            setcontrast()
        elif choice == 3:
            setexposure()
        elif choice == 4:
            setwb()
        elif choice == 5:
            if flash:
                flash = False
            else:
                flash = True
        elif choice == 9:
            ## Write code to set all defaults here
            cam.brightness = 50
            cam.contrast = 0
            cam.exposure_mode = 'auto'
            cam.awb_mode = 'auto'
            flash = False
            print()
            print("All values set back to their defaults!")
            sleep(2)
        elif choice == 0:
            return
        else:
            print("Invalid choice!")
            sleep(1)

def acap_menu():
    # Generates the menu to kick off automatic data capture
    subheader("Automatic Data Capture")

    pi = input("Polling interval tick time in seconds (default=1)?   ")
    ci = input("Capture image every X ticks (0 for none [default])?  ")
    pp = input("Total polling period is X ticks long (default=3600)? ")

    poll_interval = 1
    cap_interval = 0
    poll_period = 3600

    if pi:
        poll_interval = float(pi)
    if ci:
        cap_interval = int(ci)
    if pp:
        poll_period = int(pp)

    acapSession = threading.Thread(target=acap, args=(poll_interval, cap_interval, poll_period))
    acaps.append(acapSession)
    acapSession.start()

def acap(poll_interval, cap_interval, poll_period):
    # Performs automatic capture of sensor data & pictures
    filename = "{}_ACAP_{}.csv".format(sessionName, strftime("%Y%m%d-%H%M%S"))
    subheader("Automatic Data Capture")
    autocaptures = []

    with open("{}/{}".format(sessionPath, filename), mode='w') as file:
        dx = csv.writer(file)
        dx.writerow(["T", "LTime", "Pressure", "Depth", "ETemp", "ITemp"])
        logging.info("Automatic data capture under file name " + filename + " has begun.")
        for tick in range(1, poll_period + 1):
            startTime = time()
            ltime, pressure, depth, etemp, itemp = getReadings()
            dx.writerow([tick, ltime, pressure, depth, etemp, itemp])

            if cap_interval != 0 and tick % cap_interval == 0:
                autocap = threading.Thread(target=capture, args=("auto",), daemon=False)
                autocaptures.append(autocap)
                autocap.start()

            # This block ensures that the requested tick rate is accurate by
            # factoring in how long it took for the tick to process before
            # sleeping.
            if (time() - startTime) >= poll_interval:
                logging.debug("ACAP tick took longer than prescribed tick time!")
            else:
                sleep(poll_interval-(time()-startTime))
            tick += 1
    logging.info("Automatic data capture has ended.")
    return

def isAcap():
    for t in acaps:
        if t.is_alive():
            return True
    return False

def quitMCD():
    # Gracefully closes the program
    if isAcap():
        print()
        print("ACAP is currently active! Quitting is not recommended.")
        sleep(2)
        return
    gpio.output(lamp, False)
    logging.info("User-invoked QUIT")
    sys.exit()

def netvidHandler():
    # Drives the network video stream for live viewing by the SCU.
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 19212))
    server_socket.listen(5)

    while True:
        sessions = []
        connection = server_socket.accept()[0].makefile('wb')
        session = threading.Thread(target=netStream, args=(connection,), daemon=True)
        sessions.append(session)
        session.start()

    server_socket.close()

def netStream(connection):
    # Sustains a live streaming session when SCU connects to video feed.
    def closeConnect(reason):
        logging.debug("Attempting to close netStream connection ({})...".format(reason))
        try:
            cam.stop_recording()
        except:
            pass
        try:
            connection.close()
        except:
            pass

    cam.resolution = (1280, 720)
    cam.framerate = 24
    cam.start_recording(connection, format='h264')
    run = True
    while run:
        buildAnnotate()
        try:
            cam.wait_recording(1)
        except BrokenPipeError:
            closeConnect("Broken Pipe")
            run = False
        except ConnectionResetError:
            closeConnect("Connection Reset")
            run = False

def toggleLamp():
    # Toggles the lamp state on or off
    if gpio.input(lamp):
        gpio.output(lamp, False)
    else:
        gpio.output(lamp, True)

def buildAnnotate():
    # Builds the annotation string for the camera
    ltime, pressure, depth, etemp, itemp = getReadings()
    cam.annotate_background = picamera.Color('black')
    cam.annotate_text = "Time: {} | Pressure: {}mbar | Depth: {}m | ETemp: {}C | ITemp {}C".format(ltime, pressure, depth, etemp, itemp)


# Initialization
headertable = PrettyTable()
headertable.field_names = ["Local Time", "Pressure (millibars)", "Depth (meters)", "External Temp", "Internal Temp"]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(logfile)
    ]
)
logging.info("MCD has started.")

cam = picamera.PiCamera()
cam.rotation = camrot
streamThread = threading.Thread(target=netvidHandler, daemon=True)
streamThread.start()
acaps = []

lamp = 4       # GPIO pin for the lamp controller
flash = False  # Determines if lamp should be lit when capturing pictures
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(lamp, gpio.OUT)
gpio.output(lamp, False)

print()
sessionName = input("What is the name of this session? ")
sessionPath = "{}/{}".format(fileroot, sessionName)
os.system("mkdir {}".format(sessionPath))
sessionFile = "{}_passiveCap_{}.csv".format(sessionName, strftime("%Y%m%d-%H%M%S"))
sessionFullFile = "{}/{}".format(sessionPath, sessionFile)
with open(sessionFullFile, mode='a') as file:
    dx = csv.writer(file)
    dx.writerow(["LTime", "Pressure", "Depth", "ETemp", "ITemp", "Notes"])
logging.info("MCD session " + sessionName + " has been initialized.")


# Main Loop
while True:
    refreshUI()
    choice = int(input("Please choose a command: "))
    if choice == 1:
        print("Capturing picture...")
        capfile = capture("manual")
        print("Captured as {}".format(capfile))
        sleep(2)
        refreshUI()
    elif choice == 2:
        acap_menu()
    elif choice == 3:
        camsettings()
    elif choice == 4:
        print()
        note = input("Write your note here: ")
        writeLog(note)
        refreshUI()
    elif choice ==5:
        toggleLamp()
    elif choice == 9:
        refreshUI()
    elif choice == 0:
        quitMCD()
    else:
        print ("Invalid choice!")
        sleep(1)
