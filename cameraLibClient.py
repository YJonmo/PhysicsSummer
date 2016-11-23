'''
Library for the control of the Raspberry Pi camera module using picamera.

Author: Damon Hutley
Date: 21st November 2016
'''

try:
	from picamera import PiCamera
	picam = 1
except RuntimeError:
	print("Picamera not found")
	picam = 0
import socket
import time


class cameraModuleClient:
	
	def __init__(self):
		'''
		Initialise the camera module class with picamera.
		'''
		
		# Create an instance of the Picamera class
		if picam == 1:
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
		client_socket.connect(('172.24.94.238', 8000))
		
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
		
	
	def recv_msg(sock):
		'''
		Receive a message from the network.
		'''
		
		# Read message length and unpack it into an integer
		raw_msglen = recvall(sock, 4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# Read the message data
		return recvall(sock, msglen)
		
	
	def recvall(sock, n):
		'''
		Decode the message given the message length.
		'''
		
		# Helper function to recv n bytes or return None if EOF is hit
		data = ''
		while len(data) < n:
			packet = sock.recv(n - len(data))
			if not packet:
				return None
			data += packet
		return data
	   
	
	def receiveCommand(self):
		'''
		Control the camera remotely from a network computer.
		'''
		
		# Initialise the socket connection
		client_socket = socket.socket()
		client_socket.connect(('172.24.94.238', 8000))
		
		# Recieve data from host
		#command = client_socket.recv(1024)
		print("Waiting for message...")
		command = self.recv_msg(client_socket)
		print("Command received!")
		
		# Perform command
		if command == "I":
			capturePhoto()
		elif command == "V":
			#duration = client_socket.recv(1024)
			duration = self.recv_msg(client_socket)
			captureStream(duration)
		elif command == "S":
			#duration = client_socket.recv(1024)
			duration = self.recv_msg(client_socket)
			client_socket.close()
			networkStreamClient(duration)
			client_socket = socket.socket()
			client_socket.connect(('172.24.94.238', 8000))
		elif command == "R":
			#width = client_socket.recv(1024)
			width = self.recv_msg(client_socket)
			#height = client_socket.recv(1024)
			height = self.recv_msg(client_socket)
			setResolution(width, height)
		elif command == "F":
			#rate = client_socket.recv(1024)
			rate = self.recv_msg(client_socket)
			setFrameRate(rate)
		elif command == "X":
			#speed = client_socket.recv(1024)
			speed = self.recv_msg(client_socket)
			setExposureTime(speed)
		
	
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
		
