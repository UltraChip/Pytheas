# Pytheas

Main repository for the Pytheas submersible probe system. 

**List of Acronyms/Terms**
- **USP**  - Underwater Sensor Platform - The primary platform in the Pytheas system; a water-proofed and pressure-rated sensor pod designed to be deployed in deep water.
- **SCU**  - Surface Control Unit       - Surface-based platform for communicating and controlling the USP.
- **PCS**  - Pytheas Control System     - Primary operating software for the USP, provides live manual interface as well as autonomous operation.
- **ACAP** - Autonomous Capture         - Shorthand for csv capture files generated in autonomous mode.
- **Passive**         - As in, passive captures. Shorthand for the standard csv capture file generated for each session recording any instance the sensors are manually polled.

**Installation Instructions**

*Work in Progress* - I plan to write a script(s?) to automate the installation process soon. In the meantime, consider these bare-bones instructions for the USP:
1. Start with a Raspberry Pi imaged with PiOS and wired according to the block diagram in this repository.
2. In raspi-config make sure that the I2C and camera module interfaces are enabled. I also STRONGLY recommend resetting GPU memory allocation to 256MB.
3. Configure eth0 for a static IP address (recommend 192.168.2.2/24)
4. Ensure all of the dependencies (listed below) are installed.
5. Clone this repository to a convenient location (recommended: ~/pytheas)
6. Review the "quick values" in pcs.py and make sure they are configured to your liking. It's strongly recommended that auxPath be set to wherever you're mounting the SCU's NFS share, because otherwise it kinda defeats the purpose.
7. Add the SCU to your /etc/hosts file under a convenient name (recommended: pytheas-scu or just scu)

Likewise, consider this the bare-bones instructions for the SCU:
1. Start with a machine imaged with a desktop Linux distribution (tested on Linux Mint 20.1 but will probably work on most major distributions)
2. Configure an ethernet network interface with a static IP address (recommend 192.168.2.1/24)
3. Ensure all of the dependencies (listed below) are installed.
4. Configure /etc/exports to host a directory the USP can use to copy backups to (recommended: /usp-backups)
5. Clone this repository to a convenient location (recommended: ~/pytheas)
6. Review the contents of .scu-commands and correct any/all path references to suit your personal set up. 
7. Either copy/paste the contents of .scu-commands in to your .bashrc file or just have your .bashrc directly reference .scu-commands
8. Add the USP to your /etc/hosts file under a convenient name (recommended: pytheas-usp or just usp)

**Dependencies for USP**
- Python 3
- PrettyTable python library
- python-smbus library (needed for ms5837-python)
- Screen
- OpenSSH Server

**Dependencies for SCU**
- VLC
- nfs-kernel-server

**SCU COMMANDS**

These commands can be issued from the SCU terminal window
- **start-pcs**    - Initializes the PCS software on the USP
- **start-stream** - Brings up the live video stream in a VLC window
- **dl-usp**       - Bulk-downloads ALL USP data (including session data and pcs.log) in to the SCU
- **purge-usp**    - Bulk-deletes ALL USP data (including session data and pcs.log) from the SCU

**CSV Fields**
- **T**        - Time Index - Number of ticks since the capture session began. Can be used as a key value if importing in to DBs. Note that the T field is only present on autonomous data captures.
- **LTime**    - Local Time - The time of day that the record was captured. Based off of whatever time zone is configured in the USP.
- **Pressure** - The water pressure at the time of capture. Measured in millibars.
- **Depth**    - The depth of the USP at time of capture, computed from the pressure reading. Measured in meters.
- **ETemp**    - External Temperature - The water temperature at time of capture, measured in Celcius.
- **ITemp**    - Internal Temperature - Internal USP temperature as reported by the CPU. Measured in Calcius.
- **Notes**    - Free-form notes written by the operator. The notes field is only present on passive data captures.
