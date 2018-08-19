
#
#
# configuration file - contains customization for exact system
# JCS 06/07/2014
#
serverURL = "http://example.example.com:9600"

DEBUG = True

#LIGHT_BRIGHTNESS_SENSITIVITY = 2.0
#LIGHT_DISTANCE_SENSITIVITY = 2.0
# configuration for house
# list of iBeacons with x,y coordinates.  Top left corner of image is 0,0
# list of lists
# Beacon format:
#     BeaconNumber, LocalName, x, y, UDID, Major, Minor, Measured Power (from spec), x in px, y in px
# BeaconNumber is incremental from 0 up.  Don't skip a number

#pix converter
resolution = 0.1

def pixelConv(pixels):
	return pixels * resolution    # in meters

def meterToPixel(meters):
	return int(meters / resolution)    # in pixels 

BeaconList=[]
BeaconCount = 0
UUID = "2f234454cf6d4a0fadf2f4911ba9ffa6" 

#blue
x1 = 0 
y1 = 1

#red
x2 = -0.5
y2 = -0.865

#black
x3 = 0.5
y3 = -0.865

MP = -76 #Default Measured Power

# Beacon format:
#     BeaconNumber, LocalName, x, y, UDID, Major, Minor, Measured Power (from spec), x in px, y in px
Beacon = [BeaconCount,"blue", x1, y1, UUID, 0, 1, -75, meterToPixel(x1), meterToPixel(y1)]
BeaconList.append(Beacon)
BeaconCount += 1

Beacon = [BeaconCount,"red", x2, y2, UUID, 0, 2, MP, meterToPixel(x2), meterToPixel(y2)]
BeaconList.append(Beacon)
BeaconCount += 1

Beacon = [BeaconCount,"black", x3, y3, UUID, 0, 3, -70, meterToPixel(x3), meterToPixel(y3)]
BeaconList.append(Beacon)




