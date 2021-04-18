## PYTHEAS MANUAL CONTROL DECK
##
## Primary control interface for the Pytheas
## Underwater Sensor Platform (USP).

from prettytable import PrettyTable
from time import strftime, sleep
import os, subprocess, sys
import logging

def dummy(func_name):
    # Provides dummy output (and a log message) for functions that aren't fully developed yet
    logging.debug(func_name + " was called.")
    return True

def header():
    # Prints header
    os.system('clear')
    print ("+------------------------------------------------------------------------------------+")
    print ("|                                MANUAL CONTROL DECK                                 |")

def refreshUI():
    # Prints the main menu
    headertable.clear_rows()
    ltime, pressure, depth, etemp, itemp = getReadings()
    headertable.add_row([ltime, str(pressure) + " mbar", str(depth) + " m", str(etemp) + " C", str(itemp) + " C"])

    header()
    print (headertable)
    print ()
    print ("1. Capture Picture")
    print ("2. Automatic Data Capture")
    print ("3. Change Camera Settings")
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
    #itemp = dummy("getReadings-itemp")  # Use this for itemp when not running on a RasPi
    itemp = round(float(subprocess.getoutput('cat /sys/class/thermal/thermal_zone0/temp')) / 1000, 2)
    return ltime, pressure, depth, etemp, itemp

def capture():
    # Captures a single picture
    dummy("capture")

def camsettings():
    # Allows adjustment of the camera settings
    dummy("camsettings")

def acap_menu():
    # Generates the menu to kick off automatic data capture
    header()
    print ("+------------------------------------------------------------------------------------+")
    print ("|                               Automatic Data Capture                               |")
    print ("+------------------------------------------------------------------------------------+")
    print ()
    pi = input("Polling interval tick time in seconds (default=1)?   ")
    ci = input("Capture image every X ticks (0 for none [default])?  ")
    wi = input("Write-to-disk every X ticks (default = 60)?          ")
    pp = input("Total polling period is X ticks long (default=3600)? ")

    poll_interval = 1
    cap_interval = 0
    write_interval = 60
    poll_period = 3600

    if pi:
        poll_interval = int(pi)
    if ci:
        cap_interval = int(ci)
    if wi:
        write_interval = int(wi)
    if pp:
        poll_period = int(pp)

    acap(poll_interval, cap_interval, write_interval, poll_period)

def acap(poll_interval, cap_interval, write_interval, poll_period):
    # Performs automatic capture of sensor data & pictures
    dummy("acap")
    logstring = "p_int: "+str(poll_interval)+", c_int: "+str(cap_interval)+", w_int: "+str(write_interval)+", p_per: "+str(poll_period)
    logging.info(logstring)

def quitMCD():
    # Gracefully closes the MCD
    logging.info("User-invoked QUIT")
    sys.exit()


# Initialization
headertable = PrettyTable()
headertable.field_names = ["Local Time", "Pressure (millibars)", "Depth (meters)", "External Temp", "Internal Temp"]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("./mcd.log")
    ]
)
logging.info("MCD is initialized.")

while True:
    refreshUI()
    choice = int(input("Please choose a command: "))
    if choice == 1:
        capture()
    elif choice == 2:
        acap_menu()
    elif choice == 3:
        camsettings()
    elif choice == 9:
        refreshUI()
    elif choice == 0:
        quitMCD()
    else:
        print ("Invalid choice!")
        sleep(1)
