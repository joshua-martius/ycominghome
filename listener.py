import os
import os.path
from phue import Bridge
import time
import json
from datetime import datetime

config = json.loads(open("./config.json","r").read())
hue = Bridge(config["bridgeAddress"])
hue.connect()

def getTimestamp():
    time = datetime.now().strftime("%H:%M:%S")
    return "[%s]" % (time)

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
    return True

def areLightsOff():
    for group in hue.groups:
        if group.on:
            return False
    return True

def turnOnLights():
    for group in hue.groups:
        if group.name in config["groupsToTurnOn"]:
            group.on = True
    return

def setToken():
    config["atHome"] = True
    return

def removeToken():
    config["atHome"] = False
    return

def checkPing(hostnames):
    for host in hostnames:
        cmd = "timeout %.2f ping -q -c 1 %s" % (config["timeUntilTimeOut"], host)
        if os.system(cmd) == 0:
            return True
    return False

try:
    while True:
        athome = checkPing(config["devices"])
        if config["atHome"]: # if should be athome
            if athome:
                print("%s: Should be Home: Yes | Is at Home: Yes" % (getTimestamp()))
            else:
                print("%s: Should be Home: Yes | Is at Home: No" % (getTimestamp()))
                turnOffLights()
                removeToken()
                print("Turned off lights. Sleeping.")
        else: # if shouldnt be at home
            if athome:
                print("%s: Should be Home: No | Is at Home: Yes" % (getTimestamp()))
                if areLightsOff(): # if didnt come home within sleep time
                    turnOnLights()
                    setToken()
                    print("Turned on lights and set token.")
                else:
                    print("Came home within sleep time. Not turning on lights but settig token.")
                    setToken()

            else: # shouldnt be at home and isnt
                print("%s: Should be Home: No | Is at Home: No" % (getTimestamp()))
        time.sleep(config["sleeptime"])
except KeyboardInterrupt:
    json.dump(config, open("./config.json","w"))
    print("Saved current config state")