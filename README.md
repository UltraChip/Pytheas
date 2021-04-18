# Pytheas

Main repository for the Pytheas submersible probe system. 

**List of Acronyms/Terms**
- **USP** - Underwater Sensor Platform - The primary platform in the Pytheas system; a water-proofed and pressure-rated sensor pod designed to be deployed in deep water.
- **SCU** - Surface Control Unit       - Surface-based platform for communicating and controlling the USP.
- **MCD** - Manual Control Deck        - USP Control system; provides a user interface for live control.
- **ACD** - Autonomous Control Deck    - USP Control system designed to operate the USP automatically according to pre-configured settings.
- **Tethered Mode**   - Regular mode of operation; the USP is tethered to the SCU via Cat6 cable so manual operation is possible. Max operating depth is restricted by the length of the cable.
- **Autonomous Mode** - USP has no tether to the SCU and is only able to follow pre-scripted operations (via the ACD). Max operating depth is the USP's crush depth (350 meters).


**Key Files and Scripts**
- **mcd.py** - Master Control Deck. Run this on the USP for easy manual control of the platform. 

**CSV Fields**
- **T**        - Time Index - Number of ticks since the capture session began. Can be used as a key value if importing in to DBs.
- **LTime**    - Local Time - The time of day that the record was captured. Based off of whatever time zone is configured in the USP.
- **Pressure** - The water pressure at the time of capture. Measured in millibars.
- **Depth**    - The depth of the USP at time of capture, computed from the pressure reading. Measured in meters.
- **ETemp**    - External Temperature - The water temperature at time of capture, measured in Celcius.
- **ITemp**    - Internal Temperature - Internal USP temperature as reported by the CPU. Measured in Calcius.

**Dependencies for USP**
- Python 3
- PrettyTable python library

