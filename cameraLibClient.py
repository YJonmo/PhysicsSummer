'''
Library for the control of the Raspberry Pi camera module using picamera.

Author: Damon Hutley
Date: 21st November 2016
'''


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
		
	
	def setResoltion(self, width, height):
		'''
		Set the resolution of the camera
		'''
		
		# Change the resolution of the camera
		self.camera.resolution = (width, height)
		
	
	def setFrameRate(self, rate):
		'''
		Set the framerate of the camera
		'''
		
		# Change the framerate of the camera
		self.camera.framerate = rate
		
	
	def setExposureTime(self, speed):
		'''
		Set the exposure time of the camera. Note that the shutter speed 
		must be greater than (1/framerate). A shutter speed of zero will 
		result in an automatically determined exposure time.
		'''
		
		# Change the shutter speed of the camera
		self.camera.shutter_speed = speed
		
	
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
		
		
	#def initNetwork(self):
		#'''
		#Initialise the client side network on the Raspberry Pi.
		#'''
		
		## Initialise the socket connection
		#client_socket = socket.socket()
		#client_socket.connect(('0.0.0.0', 8000))
		
		## Create a file-like object for the connection
		##connection = client_socket.makefile('wb')
		
	
	def networkStreamClient(self, duration):
		'''
		Stream a video through the network.
		'''
		
		# Initialise the socket connection
		client_socket = socket.socket()
		client_socket.connect(('0.0.0.0', 8000))
		
		# Create a file-like object for the connection
		connection = client_socket.makefile('wb')
		try:
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
			
		
	#def networkStreamClient(self, duration):
		#'''
		#Stream a video through the network.
		#'''
		
		## Warm the camera up
		#self.camera.start_preview()
		#time.sleep(2)
		
		## Record the camera for length <duration>
		#camera.start_recording(connection, format = 'h264')
		#camera.wait_recording(duration)
		#camera.stop_recording()
		
	
	def receiveCommand(self):
		'''
		Control the camera remotely from a network computer.
		'''
		
		# Initialise the socket connection
		client_socket = socket.socket()
		client_socket.connect(('0.0.0.0', 8000))
		
		# Recieve data from host
		command = client_socket.recv(1024)
		
		# Perform command
		if command == "I":
			capturePhoto()
		elif command == "V":
			captureStream()
		elif command == "S":
			client_socket.close()
			networkStreamClient()
			client_socket = socket.socket()
			client_socket.connect(('0.0.0.0', 8000))
		elif command == "R":
			setResolution()
		elif command == "F":
			setFrameRate()
		elif command == "X":
			setExposureTime()
		
	
	#def closeClient(self):
		#'''
		#Free the network resources.
		#'''
		
		## Free connection resources
		#connection.close()
		#client_socket.close()
		
	
	def closeCamera(self):
		'''
		Release the camera resources.
		'''
		
		self.camera.close()
		
