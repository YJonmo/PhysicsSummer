'''
Library for the control of the Raspberry Pi camera module using picamera.

Author: Damon Hutley
Date: 21st November 2016
'''


from io import BytesIO
from picamera import PiCamera
import socket
import time


class cameraModuleClient:
	
	def __init__(self):
		'''
		Initialise the camera module class with picamera.
		'''
		
		# Create an instance of the Picamera class
		self.camera = PiCamera()
		
	
	def setResoltion(self):
		
	
	def setFrameRate(self):
		
	
	def setExposureTime(self):
		
	
	def capturePhoto(self):
		'''
		Capture a photo and store on Pi.
		'''
		
		# Warm the camera up
		self.camera.start_preview()
		sleep(2)
		
		# Capture an image and store in file image.png. Will later add options 
		# such as resolution, exposure time, etc.
		self.camera.capture('image.png')
		
	
	def captureStream(self, duration):
		'''
		Capture a video and store on Pi.
		'''
		
		# Record the camera for length <duration>, and store in file video.h264
		self.camera.start_recording('video.h264')
		self.camera.wait_recording(duration)
		self.camera.stop_recording()
		
	
	def networkStreamClient(self, duration):
		'''
		Stream a video through the network.
		'''
		
		# Initialise the socket connection
		client_socket = socket.socket()
		client_socket.connect(('my_server', 8000))
		
		# Create a file-like object for the connection
		connection = client_socket.makefile('wb')
		try:
			# Set camera parameters
			self.camera.resolution = (640, 480)
			self.camera.framerate = 24
			
			# Warm the camera up
			self.camera.start_preview()
			time.sleep(2)
			
			# Record the camera for length <duration>
			camera.start_recording(connection, format = 'h264')
			camera.wait_recording(duration)
			camera.stop_recording()
		finally:
			# Free connection resources
			connection.close()
			client_socket.close()
		
	
	def remoteControlClient(self):
		'''
		Control the camera remotely from a network computer.
		'''
		
		
	def closeCamera(self):
		'''
		Release the camera resources.
		'''
		
		self.camera.close()
		
