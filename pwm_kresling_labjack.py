"""
Code to cycle through a 100 Hz PWM output signal from 0.25 to 0.7 in increments of 0.05 on FIO0, 2, and 3
Sonia Roberts, so.roberts@northeastern.edu
PARSES group
"""
import time

from labjack import ljm

def setPWM(pwmDIO, pwmValue):
    '''
    pwmDIO: The digital IO port to address. On the LabJack T7 with no accessories,
    ports 0, 2, and 3 will work. 
    
    pwmValue: A value between 0 and 1 that represents the PWM signal to send. 
    Values between 0.3 and 0.7 will give you basically the whole range. 
    '''
    rollValue = 800000
    aNames = ["DIO_EF_CLOCK0_DIVISOR", "DIO_EF_CLOCK0_ROLL_VALUE",
              "DIO_EF_CLOCK0_ENABLE", "DIO%i_EF_ENABLE" % pwmDIO,
              "DIO%i_EF_INDEX" % pwmDIO, "DIO%i_EF_CONFIG_A" % pwmDIO,
              "DIO%i_EF_ENABLE" % pwmDIO, "DIO18_EF_ENABLE",
              "DIO18_EF_INDEX", "DIO18_EF_ENABLE"]
    aValues = [1, rollValue,
               1, 0,
               0, pwmValue * rollValue,
               1, 0,
               7, 1]
    numFrames = len(aNames)
    results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

# Open first found LabJack T7
handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier

DIOs = [0, 2, 3]

PWMs = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]

# Set each DIO pin to each PWM frequency
for PWM in PWMs:
    print("PWM:", PWM)
    for currDIO in DIOs:
        setPWM(currDIO, PWM)
    time.sleep(2)

# Set all PWM signals to 0
for currDIO in DIOs:
    setPWM(currDIO, 0)

# Turn off PWM output
for currDIO in DIOs:
    aNames = ["DIO%i_EF_ENABLE" % currDIO]
    aValues = [0]
    numFrames = len(aNames)
    results = ljm.eWriteNames(handle, numFrames, aNames, aValues)

# Close handle
ljm.close(handle)
