'''
Test for the camera module without remote connection.

Author: Damon Hutley
Date: 25th November 2016
'''

import cameraLibClient

# Initialise the camera client module
cam = cameraLibClient.cameraModuleClient()

# Set the resolution
width = 640
height = 480
cam.setResolution(width, height)

# Set the framerate
rate = 24
cam.setFrameRate(rate)

# Set the exposure time
speed = 0#30000
cam.setExposureTime(speed)

# Take a photo
cam.capturePhoto('image.png')

# Record a video
duration = 10
cam.captureStream(duration, 'video.h264')

# Free the camera resources
cam.closeCamera()
