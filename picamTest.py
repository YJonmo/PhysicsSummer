'''
A set of tests for the Raspberry Pi camera module using the Python camera library.

Author: Damon Hutley
Date: 2/12/2016
'''

import cameraLibClient

def testLowestRes(camera):
	width = 320
	height = 240
	camera.setResolution(width, height)
	camera.capturePhoto('im320x240.png')

def testLowRes(camera):
	width = 640
	height = 480
	camera.setResolution(width, height)
	camera.capturePhoto('im640x480.png')

def testMedRes(camera):
	width = 1280
	height = 720
	camera.setResolution(width, height)
	camera.capturePhoto('im1280x720.png')

def testHighRes(camera):
	width = 1920
	height = 1080
	camera.setResolution(width, height)
	camera.capturePhoto('im1920x1080.png')

def testHigherRes(camera):
	width = 2560
	height = 1440
	camera.setResolution(width, height)
	camera.capturePhoto('im2560x1440.png')

def testHighestRes(camera):
	width = 3280
	height = 2464
	camera.setResolution(width, height)
	camera.capturePhoto('im3280x2464.png')

# Initialise the camera client module
cam = cameraLibClient.cameraModuleClient()

# Camera image resolution tests
testLowestRes(cam)
testLowRes(cam)
testMedRes(cam)
testHighRes(cam)
testHigherRes(cam)
testHighestRes(cam)

# Free the camera resources
cam.closeCamera()
