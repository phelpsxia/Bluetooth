
#
#
# configuration file - contains customization for exact system
# based on JCS 06/07/2014
# modified and updated by Phelps, running locally only 08/20/2018
# using redbeacon dot as the iBeacon
#serverURL = "http://example.example.com:9600"

DEBUG = True

# configuration for house
# list of iBeacons with x,y coordinates.  left buttom corner of image is 0,0
# list of lists
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

MP0 = -76
MP1 = -68
MP2 = -73

center_x = 2
center_y = 2
#blue
x0 = center_x
y0 = center_y + 1

#red
x1 = center_x - 0.5
y1 = center_y - 0.865

#black
x2 = center_x + 0.5
y2 = center_y - 0.865

#MP = -76 #Default Measured Power

# Beacon format:
#     BeaconNumber, LocalName, x, y, UDID, Major, Minor, Measured Power (from spec), x in px, y in px
Beacon = [BeaconCount,"blue", x0, y0, UUID, 0, 1, -76, meterToPixel(x0), meterToPixel(y0)]
BeaconList.append(Beacon)
BeaconCount += 1

Beacon = [BeaconCount,"red", x1, y1, UUID, 0, 2, -68, meterToPixel(x1), meterToPixel(y1)]
BeaconList.append(Beacon)
BeaconCount += 1

Beacon = [BeaconCount,"black", x2, y2, UUID, 0, 3, -73, meterToPixel(x2), meterToPixel(y2)]
BeaconList.append(Beacon)




