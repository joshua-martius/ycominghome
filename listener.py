import os
import os.path
from phue import Bridge
import time

TOKENNAME = "./.athome"
HOSTNAME = "137.226.214.206"
SLEEPTIME = 10
groupsToTurnOn = ["Wohnzimmer"]
hue = Bridge("137.226.214.9")
hue.connect()

def sendHeartbeat():
    for i in range(2):
        for group in hue.groups:
            group.on = True
        time.sleep(0.5)
        for group in hue.groups:
            group.on = False
    return

def turnOffLights():
    for group in hue.groups:
        group.on = False
    return

def turnOnLights():
    for group in hue.groups:
        if group.name in groupsToTurnOn:
            group.on = True
    return

def setToken():
    open(TOKENNAME,'a').close()
    return

def removeToken():
    os.remove(TOKENNAME)
    return

def checkPing(hostname):
    if os.system("ping -q -c 1 " + hostname) == 0:
        return True
    else:
        return False

while True:
    athome = checkPing(HOSTNAME)
    if os.path.isfile(TOKENNAME): # if should be athome
        if athome:
            print("Should be Home: Yes | Is at Home: Yes")
        else:
            print("Should be Home: Yes | Is at Home: No")
            turnOffLights()
            removeToken()
            print("Turned off lights. Sleeping.")
    else: # if shouldnt be at home
        if athome:
            print("Should be Home: No | Is at Home: Yes")
            turnOnLights()
            setToken()
            print("Turned on lights and set token.")
        else: # shouldnt be at home and isnt
            print("Should be Home: No | Is at Home: No")
    time.sleep(SLEEPTIME)