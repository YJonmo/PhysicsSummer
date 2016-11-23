'''
Library for the control of the Raspberry Pi camera module using picamera.

Author: Damon Hutley
Date: 21st November 2016
'''


# For network testing purposes
try:
	from picamera import PiCamera
	picam = 1
except RuntimeError:
	print("Picamera not found")
	picam = 0
import socket
import time
import struct


class cameraModuleClient:
	
	def __init__(self):
		'''
		Initialise the camera module class with picamera.
		'''
		
		# Create an instance of the Picamera class
		if picam == 1:
			self.camera = PiCamera()
		
	
	def setResolution(self, width, height):
		'''
		Set the resolution of the camera
		'''
		
		# Change the resolution of the camera
		if picam == 1:
			self.camera.resolution = (width, height)
		print("Resolution changed")
		
	
	def setFrameRate(self, rate):
		'''
		Set the framerate of the camera
		'''
		
		# Change the framerate of the camera
		self.camera.framerate = rate
		print("Framerate changed")
		
	
	def setExposureTime(self, speed):
		'''
		Set the exposure time of the camera. Note that the shutter speed 
		must be greater than (1/framerate). A shutter speed of zero will 
		result in an automatically determined exposure time.
		'''
		
		# Change the shutter speed of the camera
		self.camera.shutter_speed = speed
		print("Exposure Time Changed")
		
	
	def capturePhoto(self):
		'''
		Capture a photo and store on Pi.
		'''
		
		# Warm the camera up
		self.camera.start_preview()
		sleep(2)
		
		# Capture an image and store in file image.png.
		self.camera.capture('image.png')
		print("Photo captured")
		
	
	def captureStream(self, duration):
		'''
		Capture a video and store on Pi.
		'''
		
		# Record the camera for length <duration>, and store in file video.h264
		self.camera.start_recording('video.h264')
		print("Recording started...")
		self.camera.wait_recording(duration)
		self.camera.stop_recording()
		print("Recording finished")
		
		
	#def initNetwork(self):
		#'''
		#Initialise the client side network on the Raspberry Pi.
		#'''
		
		## Initialise the socket connection
		#client_socket = socket.socket()
		#client_socket.connect(('0.0.0.0', 8000))
		
		## Create a file-like object for the connection
		##connection = client_socket.makefile('wb')
		
	
	def networkStreamClient(self, sock, duration):
		'''
		Stream a video through the network.
		'''
		
		# Initialise the socket connection
		#client_socket = socket.socket()
		#client_socket.connect(('172.24.94.238', 8000))
		
		# Create a file-like object for the connection
		connection = sock.makefile('wb')
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
			#client_socket.close()
			
		
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
		
	
	def send_msg(self, sock, msg):
		'''
		Send message with a prefixed length.
		'''
		
		# Prefix each message with a 4-byte length (network byte order)
		msg = struct.pack('>I', len(msg)) + msg
		sock.sendall(msg)
		
	
	def recv_msg(self, sock):
		'''
		Receive a message from the network.
		'''
		
		# Read message length and unpack it into an integer
		raw_msglen = self.recvall(sock, 4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# Read the message data
		return self.recvall(sock, msglen)
		
	
	def recvall(self, sock, n):
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
	   
	
	def initNetwork(self):
		'''
		Initialise the client side network on the Raspberry Pi.
		'''
		
		# Initialise the socket connection
		self.client_socket = socket.socket()
		print("Waiting for connection...")
		self.client_socket.connect(('172.24.94.238', 8000))
		print("Connection accepted!")
		
	
	def receiveCommand(self):
		'''
		Control the camera remotely from a network computer.
		'''
		
		# Initialise the socket connection
		#client_socket = socket.socket()
		#print("Waiting for connection...")
		#client_socket.connect(('172.24.94.238', 8000))
		#print("Connection accepted!")
		
		# Recieve data from host
		#command = client_socket.recv(1024)
		print("Waiting for command...")
		command = self.recv_msg(self.client_socket)
		print("Command received: " + command)
		
		# Perform command
		if command == "I":
			self.capturePhoto()
		elif command == "V":
			#duration = client_socket.recv(1024)
			print("Waiting for duration...")
			duration = int(self.recv_msg(self.client_socket))
			print("Duration: " + str(duration))
			self.captureStream(duration)
		elif command == "S":
			#duration = client_socket.recv(1024)
			print("Waiting for duration...")
			duration = int(self.recv_msg(self.client_socket))
			print("Duration: " + str(duration))
			#client_socket.close()
			self.networkStreamClient(self.client_socket, duration)
			#client_socket = socket.socket()
			#client_socket.connect(('172.24.94.238', 8000))
		elif command == "R":
			#width = client_socket.recv(1024)
			print("Waiting for width...")
			width = int(self.recv_msg(self.client_socket))
			print("Width: " + str(width))
			#height = client_socket.recv(1024)
			print("Waiting for height...")
			height = int(self.recv_msg(self.client_socket))
			print("Height: " + str(height))
			self.setResolution(width, height)
			self.send_msg(self.client_socket, "Resolution changed")
		elif command == "F":
			#rate = client_socket.recv(1024)
			print("Wating for framerate...")
			rate = int(self.recv_msg(self.client_socket))
			print("Framerate: " + str(rate))
			self.setFrameRate(rate)
		elif command == "X":
			#speed = client_socket.recv(1024)
			print("Waiting for shutter speed...")
			speed = int(self.recv_msg(self.client_socket))
			print("Shutter Speed: " + str(speed))
			self.setExposureTime(speed)
		elif command == "Q":
			print("Closing socket...")
			self.client_socket.close()
		
		return command
		
	
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
		if picam == 1:
			self.camera.close()
		
