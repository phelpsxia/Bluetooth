#!/usr/bin/python

# BeaconAir - Reads iBeacons and controls HUE lights
# JCS  6/7/14
#
#
import sys
import time
import utils

sys.path.append('./ble')
sys.path.append('./config')

# if conflocal.py is not found, import default conf.py

# Check for user imports
import config as conf





import bleThread

#import lights
import webmap
import bubblelog
import iBeaconChart

from threading import Thread
from Queue import Queue

# State Variables

currentiBeaconRSSI=[]
rollingiBeaconRSSI=[]
currentiBeaconTimeStamp=[]

# Light State Variables

#currentLightState= []

#LIGHT_BRIGHTNESS_SENSITIVITY = 2.0
#LIGHT_DISTANCE_SENSITIVITY = 2.0
BEACON_ON = True
DISPLAY_BEACON_ON = True
#DISPLAY_LIGHTS_ON = True

# init state variables
for beacon in conf.BeaconList:
	currentiBeaconRSSI.append(0)
	rollingiBeaconRSSI.append(0)
	currentiBeaconTimeStamp.append(time.time())


# recieve commands from RasPiConnect Execution Code

def completeCommand():

        f = open("/home/phelps/BeaconAir/state/BeaconAirCommand.txt", "w")
        f.write("DONE")
        f.close()

def processCommand():
	global LIGHT_BRIGHTNESS_SENSITIVITY
	global LIGHT_DISTANCE_SENSITIVITY
	global BEACON_ON
	global DISPLAY_BEACON_ON
	global DISPLAY_LIGHTS_ON
	global currentLightState

        f = open("/home/phelps/BeaconAir/state/BeaconAirCommand.txt", "r")
        command = f.read()
        f.close()

        if (command == "") or (command == "DONE"):
                # Nothing to do
                return False

        # Check for our commands

        print "Processing Command: ", command

        if (command == "BEACONON"):
                BEACON_ON = True
                completeCommand()
                return True

        if (command == "BEACONOFF"):
                BEACON_ON = False
                completeCommand()
                return True

        if (command == "DISPLAYBEACONON"):
                DISPLAY_BEACON_ON = True
                completeCommand()
                return True

        if (command == "DISPLAYBEACONOFF"):
                DISPLAY_BEACON_ON = False
                completeCommand()
                return True

# build configuration Table


# set up BLE thread
# set up a communication queue



queueBLE = Queue()
BLEThread = Thread(target=bleThread.bleDetect, args=(__name__,10,queueBLE,))
BLEThread.daemon = True
BLEThread.start()

bubblelog.writeToBubbleLog("BeaconAir Started") 

# the main loop of BeaconAir
myPosition = [0,0]
lastPosition = [1,1]
beacons = []
while True:
	if (BEACON_ON == True):
		# check for iBeacon Updates
		print "Queue Length =", queueBLE.qsize()
		if (queueBLE.empty() == False):
			result = queueBLE.get(False)
			print "------"
			print "currentiBeaconRSSI", currentiBeaconRSSI
			utils.processiBeaconList(result,currentiBeaconRSSI, currentiBeaconTimeStamp,rollingiBeaconRSSI)
			utils.clearOldValues(10,currentiBeaconRSSI, currentiBeaconTimeStamp,rollingiBeaconRSSI)
			#print conf.BeaconList
			for beacon in conf.BeaconList:
				utils.printBeaconDistance(beacon, currentiBeaconRSSI, currentiBeaconTimeStamp,rollingiBeaconRSSI)
			# update position
			if (utils.haveThreeGoodBeacons(rollingiBeaconRSSI) >= 3):
				oldbeacons = beacons	
				beacons = utils.get3ClosestBeacons(rollingiBeaconRSSI)
				print "beacons=", beacons	
				if (cmp(oldbeacons, beacons) != 0):	
					bubblelog.writeToBubbleLog("closebeacons:%i,%i,%i" % (beacons[0], beacons[1], beacons[2]))
				
				# setup for Kludge
				#rollingiBeaconRSSI[7] = rollingiBeaconRSSI[6]

				myPosition = utils.getXYFrom3Beacons(beacons[0],beacons[1],beacons[2], rollingiBeaconRSSI)
				print "myPosition1 = %3.2f,%3.2f" % (myPosition[0], myPosition[1])
				#bubblelog.writeToBubbleLog("position updated:%3.2f,%3.2f" % (myPosition[0], myPosition[1]))
			
				# calculate jitter in position	
				jitter = (((lastPosition[0] - myPosition[0])/lastPosition[0]) + ((lastPosition[1] - myPosition[1])/lastPosition[1]))/2.0 
				jitter = jitter * 100.0   # to get to percent
				lastPosition = myPosition 
				print "jitter=", jitter
			
				f = open("/home/pi/BeaconAir/state/distancejitter.txt", "w")
					
				f.write(str(jitter))
				f.close()

				# build webpage
				#webmap.buildWebMapToFile(myPosition, rollingiBeaconRSSI, currentLightState, DISPLAY_BEACON_ON, DISPLAY_LIGHTS_ON)
	
				# build beacon count graph
				iBeaconChart.iBeacondetect(rollingiBeaconRSSI)
			else:
				# lost position
				myPosition = [-myPosition[0], -myPosition[1]]	

		#print currentiBeaconRSSI
		#print currentiBeaconTimeStamp

	# end of BEACON_ON - always process commands
	else:
		if (queueBLE.empty() == False):
			result = queueBLE.get(False)
		print "------"
		print "Beacon Disabled"
        # process commands from RasPiConnect
		
        #processCommand()

	time.sleep(0.25)
