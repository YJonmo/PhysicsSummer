'''
Latency test for the camera trigger function of the picamera module.

Author: Damon Hutley
Date: 16th December 2016
'''

import cameraLibServer

# Initialise the camera module
cam = cameraLibServer.cameraModuleServer()

# Enter trigger mode
cam.captureTrigger()

# Free camera resources
cam.closeCamera()
