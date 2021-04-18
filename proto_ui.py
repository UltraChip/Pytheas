## PrettyTable Test
##
## Just screwing around with PrettyTable library

from prettytable import PrettyTable
from time import strftime
from time import sleep
import random
import os

table = PrettyTable()
header = PrettyTable()
table.field_names = ["Local Time", "Pressure (millibars)", "Depth (meters)", "External Temp", "Internal Temp"]
header.field_names = ["                    PYTHEAS MANUAL CONTROL DECK"]

i = 0
while i < 1:
    os.system('clear')
    i += 1
    curtime = strftime("%H:%M:%S")
    pressure = random.randint(100,500)
    depth = round(random.uniform(10,100), 2)
    etemp = round(random.uniform(20,80), 1)
    itemp = round(random.uniform(20,80), 1)
  
    table.add_row([curtime, str(pressure) + " mbar", str(depth) + " m", str(etemp) + " C", str(itemp) + " C"])

print ("+------------------------------------------------------------------------------------+")
print ("|                             PYTHEAS MANUAL CONTROL DECK                            |")
print ("+------------------------------------------------------------------------------------+")
print ()
print (table)
print ()
print ("1. Toggle Lamp (Currently ON)")
print ("2. Start Livestream")
print ("3. Kill Livestream")
print ("4. Refresh Sensor Read")
print ()
print ("Which one? ")