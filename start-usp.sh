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

# Give a small delay to make sure everything initiates nicely
echo
echo "Waiting 5 seconds. . ."
sleep 5s
echo

# Kick off PCS
python3 /home/chip/pytheas/pcs.py