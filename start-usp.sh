#!/bin/bash

## START-USP
##
## A wrapper script to prepare the environment
## for the main PCS script


sessions="/mnt/sessions"  # Location of sessions directory
auxdir="/backups"         # Location of backup directory mountpoint

# Make sure the sessions directory exists
if [ ! -d $sessions ]; then
        mkdir $sessions
        echo -e "\n\n$sessions didn't exist, so it was created."
fi

# Mount the NFS share used to back up files
sudo mount scu:/usp-backups $auxdir
echo -e "\nMounted SCU backup share to $auxdir"

# Check the date/time and reset if neccessary
echo -e "\nThe current date is $(date +%m/%d/%Y)"
echo -e "The current time is $(date +%H:%M)\n"

read -p "Enter time in format YYYY-MM-DD HH:MM:SS (or enter for no change): " timestamp
if [ -n $timestamp ]; then
    sudo date -s "$timestamp"
fi

# Kick off PCS
python3 /home/chip/pytheas/pcs.py