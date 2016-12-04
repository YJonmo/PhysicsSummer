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
import os

NETWORK = 0 # Set to 1 if connected to network

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
		Set the resolution of the camera.
		'''
		
		# Change the resolution of the camera
		if picam == 1:
			self.camera.resolution = (width, height)
		print("Resolution changed")
		
	
	def setFrameRate(self, rate):
		'''
		Set the framerate of the camera.
		'''
		
		# Change the framerate of the camera
		if picam == 1:
			self.camera.framerate = rate
		print("Framerate changed")
		
	
	def setExposureTime(self, speed):
		'''
		Set the exposure time of the camera. Note that the shutter speed 
		must be greater than (1/framerate). A shutter speed of zero will 
		result in an automatically determined exposure time.
		'''
		
		# Change the shutter speed of the camera (in microseconds)
		if picam == 1:
			self.camera.shutter_speed = speed
		print("Exposure time changed")
		
	
	def setSharpness(self, sharpness):
		'''
		Set the sharpness level of the camera. Min: -100, Max: 100.
		'''
		if picam == 1:
			self.camera.sharpness = sharpness
		print("Sharpness changed")
		
	
	def setContrast(self, contrast):
		'''
		Set the contrast level of the camera. Min: -100, Max: 100.
		'''
		if picam == 1:
			self.camera.contrast = contrast
		print("Contrast changed")
		
	
	def setBrightness(self, brightness):
		'''
		Set the brightness level of the camera. Min: 0, Max: 100.
		'''
		if picam == 1:
			self.camera.brightness = brightness
		print("Brightness changed")
		
	
	def setSaturation(self, saturation):
		'''
		Set the saturation level of the camera. Min: -100, Max: 100.
		'''
		if picam == 1:
			self.camera.saturation = saturation
		print("Saturation changed")
		
	
	def setGain(self, gain):
		'''
		Set the gain level of the camera. If ISO is set to zero, then the 
		gain will be chosen automatically. Min: 0, Max: 800.
		'''
		if picam == 1:
			self.camera.iso = gain
		print("Gain changed")
		
	
	def capturePhoto(self, fname):
		'''
		Capture a photo and store on Pi.
		'''
		
		if picam == 1:
			# Warm the camera up
			self.camera.start_preview()
			time.sleep(2)
			
			# Capture an image and store in file <fname>
			self.camera.capture(fname)
		print("Photo captured")
		
	
	def captureStream(self, duration, fname):
		'''
		Capture a video and store on Pi.
		'''
		
		if picam == 1:
			self.camera.start_preview()
			time.sleep(2)
			
			# Record the camera for length <duration>, and store in file <fname>
			self.camera.start_recording("input.h264")
			#self.camera.start_recording(fname)
			print("Recording started...")
			self.camera.wait_recording(duration)
			self.camera.stop_recording()
		else:
			# Pretend to record (for testing purposes)
			time.sleep(duration)
		print("Recording finished")
		
		rate = str(self.camera.framerate)
		width = str(self.camera.resolution[0])
		height = str(self.camera.resolution[1])
		
		comStr = "avconv -i input.h264 -f rawvideo - | avconv -y -f rawvideo -r:v " + rate + " -s:v " + width + "x" + height + " -i - " + fname
		os.system(comStr)
		os.system("rm input.h264")
		
	
	def networkStreamClient(self, sock, duration):
		'''
		Stream a video through the network.
		'''
		
		if NETWORK == 1:
			# Create a file-like object for the connection
			connection = sock.makefile('wb')
			try:
				if picam == 1:
					# Warm the camera up
					self.camera.start_preview()
					time.sleep(2)
					
					# Record the camera for length <duration>
					camera.start_recording(connection, format = 'h264')
					camera.wait_recording(duration)
					camera.stop_recording()
				else:
					# Pretend to record (for testing purposes)
					time.sleep(duration+2)
			finally:
				# Free connection resources
				connection.close()
		
	
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
		'''self.client_socket = socket.socket()
		print("Waiting for connection...")
		self.client_socket.connect(('', 8000))
		print("Connection accepted!")'''
		
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.client_socket.bind(('',8000))
		NETWORK = 1
		
	
	def closeNetwork(self):
		'''
		Close the client side network on the Raspberry Pi.
		'''
		
		self.client_socket.close()
		NETWORK = 0
	
	def printCommands(self):
		'''
		Print a list of commands.
		'''
		
		print("\nList of commands: ")
		print("    B: Set brightness")
		print("    C: Set contrast")
		print("    F: Set framerate")
		print("    G: Set gain")
		print("    H: Help")
		print("    I: Capture an image")
		print("    N: Stream to network")
		print("    Q: Quit program")
		print("    R: Set resolution")
		print("    S: Set sharpness")
		print("    T: Set saturation")
		print("    V: Capture a video")
		print("    X: Set exposure time\n")
		
	
	def receiveCommand(self):
		'''
		Control the camera remotely from a network computer, or from the 
		Raspberry Pi terminal.
		'''
		
		if NETWORK == 1:
			# Recieve data from host
			print("Waiting for command...")
			command = self.recv_msg(self.client_socket)
			print("Command received: " + command)
		else:
			# Wait for command from Pi
			command = str(raw_input("Input camera command: ")).upper()
		
		# Perform command
		# Capture photo
		if command == "I":
			if NETWORK == 1:
				print("Waiting for filename...")
				fname = self.recv_msg(self.client_socket)
				print("Filename: " + fname)
			else:
				fname = str(raw_input("Filename: "))
			
			self.capturePhoto(fname)
			
			if NETWORK == 1:
				self.send_msg(self.client_socket, "Photo captured")
			else:
				print("Photo captured")
		
		# Capture stream
		elif command == "V":
			if NETWORK == 1:
				print("Waiting for duration...")
				duration = int(self.recv_msg(self.client_socket))
				print("Duration: " + str(duration))
				print("Waiting for filename...")
				fname = self.recv_msg(self.client_socket)
				print("Filename: " + fname)
			else:
				duration = input("Duration: ")
				fname = str(raw_input("Filename: "))
			self.send_msg(self.client_socket, "Recording started...")
			self.captureStream(duration, fname)
			self.send_msg(self.client_socket, "Recording finished")
		
		# Network stream
		elif command == "S":
			if NETWORK == 1:
				print("Waiting for duration...")
				duration = int(self.recv_msg(self.client_socket))
				print("Duration: " + str(duration))
				self.networkStreamClient(self.client_socket, duration)
			else:
				print("Not connected to network")
		
		# Change resolution
		elif command == "R":
			print("Waiting for width...")
			width = int(self.recv_msg(self.client_socket))
			print("Width: " + str(width))
			print("Waiting for height...")
			height = int(self.recv_msg(self.client_socket))
			print("Height: " + str(height))
			self.setResolution(width, height)
			self.send_msg(self.client_socket, "Resolution changed")
		
		# Change framerate
		elif command == "F":
			print("Wating for framerate...")
			rate = int(self.recv_msg(self.client_socket))
			print("Framerate: " + str(rate))
			self.setFrameRate(rate)
			self.send_msg(self.client_socket, "Framerate changed")
			
		# Change exposure time
		elif command == "X":
			print("Waiting for shutter speed...")
			speed = int(self.recv_msg(self.client_socket))
			print("Shutter Speed: " + str(speed))
			self.setExposureTime(speed)
			self.send_msg(self.client_socket, "Exposure time changed")
			
		# Quit program
		elif command == "Q":
			if NETWORK == 1:
				print("Closing socket...")
				self.closeNetwork()
			
		else:
			print("Not a command")
		
		return command
		
	
	def closeCamera(self):
		'''
		Release the camera resources.
		'''
		
		# Turn off the camera
		if picam == 1:
			self.camera.close()
		
