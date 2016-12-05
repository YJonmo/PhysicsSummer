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
import sys

NETWORK = 0 # Set to 1 if connected to network

BRIGHTNESS_MIN = 0
BRIGHTNESS_MAX = 100
CONTRAST_MIN = -100
CONTRAST_MAX = 100
SATURATION_MIN = -100
SATURATION_MAX = 100
SHARPNESS_MIN = -100
SHARPNESS_MAX = 100
GAIN_MIN = 0
GAIN_MAX = 1600
WIDTH_MIN = 64
WIDTH_MAX = 3280
HEIGHT_MIN = 64
HEIGHT_MAX = 2464
DURATION_MIN = 0
DURATION_MAX = sys.maxint
FRAMERATE_MIN = 0.1
FRAMERATE_MAX = 90

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
		
	
	def setFrameRate(self, rate):
		'''
		Set the framerate of the camera.
		'''
		
		# Change the framerate of the camera
		if picam == 1:
			self.camera.framerate = rate
		
	
	def setExposureTime(self, speed):
		'''
		Set the exposure time of the camera. Note that the shutter speed 
		must be greater than (1/framerate). A shutter speed of zero will 
		result in an automatically determined exposure time.
		'''
		
		# Change the shutter speed of the camera (in microseconds)
		if picam == 1:
			self.camera.shutter_speed = speed
		
	
	def setSharpness(self, sharpness):
		'''
		Set the sharpness level of the camera. Min: -100, Max: 100.
		'''
		if picam == 1:
			self.camera.sharpness = sharpness
		
	
	def setContrast(self, contrast):
		'''
		Set the contrast level of the camera. Min: -100, Max: 100.
		'''
		if picam == 1:
			self.camera.contrast = contrast
		
	
	def setBrightness(self, brightness):
		'''
		Set the brightness level of the camera. Min: 0, Max: 100.
		'''
		if picam == 1:
			self.camera.brightness = brightness
		
	
	def setSaturation(self, saturation):
		'''
		Set the saturation level of the camera. Min: -100, Max: 100.
		'''
		if picam == 1:
			self.camera.saturation = saturation
		
	
	def setGain(self, gain):
		'''
		Set the gain level of the camera. If ISO is set to zero, then the 
		gain will be chosen automatically. Min: 0, Max: 800.
		'''
		if picam == 1:
			self.camera.iso = gain
		
	
	def capturePhoto(self, fname):
		'''
		Capture a photo and store on Pi.
		'''
		
		floc = "../Images/" + fname
		
		if picam == 1:
			# Warm the camera up
			self.camera.start_preview()
			time.sleep(2)
			
			# Capture an image and store in file <fname>
			self.camera.capture(floc)
			self.camera.stop_preview()
		
	
	def captureStream(self, duration, fname):
		'''
		Capture a video and store on Pi.
		'''
		
		if picam == 1:
			self.camera.start_preview()
			time.sleep(2)
			
			# Record the camera for length <duration>, and store in file <fname>
			self.camera.start_recording("input.h264")
			self.camera.wait_recording(duration)
			self.camera.stop_recording()
		else:
			# Pretend to record (for testing purposes)
			time.sleep(duration)
		
		# Obtain video stats
		rate = str(self.camera.framerate)
		width = str(self.camera.resolution[0])
		height = str(self.camera.resolution[1])
		
		# Convert raw h264 video into a container to enable playback at the correct framerate
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
		
	
	def inputParameter(self, parameter):
		'''
		Wait for a parameter from either the network or the Pi terminal.
		'''
		
		# Find the default, minimum, and maximum values for the parameter
		if parameter == "Brightness":
			default = self.camera.brightness
			minimum = BRIGHTNESS_MIN
			maximum = BRIGHTNESS_MAX
			
		elif parameter == "Contrast":
			default = self.camera.contrast
			minimum = CONTRAST_MIN
			maximum = CONTRAST_MAX
			
		elif parameter == "Gain":
			default = self.camera.iso
			minimum = GAIN_MIN
			maximum = GAIN_MAX
			
		elif parameter == "Saturation":
			default = self.camera.saturation
			minimum = SATURATION_MIN
			maximum = SATURATION_MAX
			
		elif parameter == "Sharpness":
			default = self.camera.sharpness
			minimum = SHARPNESS_MIN
			maximum = SHARPNESS_MAX
			
		elif parameter == "Exposure time":
			default = self.camera.shutter_speed
			minimum = 0
			maximum = int(1000000/self.camera.framerate)
			
		elif parameter == "Width":
			default = self.camera.resolution[0]
			minimum = WIDTH_MIN
			maximum = WIDTH_MAX
			
		elif parameter == "Height":
			default = self.camera.resolution[1]
			minimum = HEIGHT_MIN
			maximum = HEIGHT_MAX
			
		elif parameter == "Duration":
			default = DURATION_MIN # Will change to max once ability to escape video is added
			minimum = DURATION_MIN
			maximum = DURATION_MAX
			
		elif parameter == "Framerate":
			default = self.camera.framerate
			minimum = FRAMERATE_MIN
			maximum = FRAMERATE_MAX
		
		else:
			default = None
		
		if NETWORK == 1:
			print("Wating for " + parameter.lower() + "...")
			value = self.recv_msg(self.client_socket)
			print(parameter + ": " + str(value))
		elif default == None:
			value = str(raw_input(parameter + ": "))
		else:
			while True:
				value = str(raw_input(parameter + " (Default: " + str(default) + ", Min: " + str(minimum) + ", Max: " + str(maximum) + "): "))
				if value == "":
					value = default
					break
				else:
					try:
						if int(value) < minimum:
							print("Value is less than minimum")
						elif int(value) > maximum:
							print("Value is greater than maximum")
						else:
							break
					except ValueError:
						print("Not a number")
		
		return value
		
	
	def confirmCompletion(self, message):
		'''
		Print confirmation message of task completion.
		'''
		
		if NETWORK == 1:
			self.send_msg(self.client_socket, message)
		else:
			print(message)
		
	
	def receiveCommand(self):
		'''
		Receive a command from the network or the Pi terminal.
		'''
		
		if NETWORK == 1:
			# Recieve data from host
			print("Waiting for command...")
			command = self.recv_msg(self.client_socket)
			print("Command received: " + command)
		else:
			# Wait for command from Pi
			command = str(raw_input("Input camera command: ")).upper()
		
		return command
		
	
	def performCommand(self, command):
		'''
		Control the camera remotely from a network computer, or from the 
		Raspberry Pi terminal.
		'''
		
		# Set brightness
		if command == "B":
			brightness = int(self.inputParameter("Brightness"))
			self.setBrightness(brightness)
			self.confirmCompletion("Brightness changed")
			
		# Set contrast
		elif command == "C":
			contrast = int(self.inputParameter("Contrast"))
			self.setContrast(contrast)
			self.confirmCompletion("Contrast changed")
			
		# Set framerate
		elif command == "F":
			rate = int(self.inputParameter("Framerate"))
			self.setFrameRate(rate)
			self.confirmCompletion("Framerate changed")
		
		# Set gain
		elif command == "G":
			gain = int(self.inputParameter("Gain"))
			self.setGain(gain)
			self.confirmCompletion("Gain changed")
			
		# Help
		elif command == "H":
			self.printCommands()
			
		# Capture photo
		elif command == "I":
			fname = self.inputParameter("Filename")
			self.capturePhoto(fname)
			self.confirmCompletion("Image captured")
				
		# Network stream
		elif command == "N":
			if NETWORK == 1:
				duration = int(self.inputParameter("Duration"))
				self.networkStreamClient(self.client_socket, duration)
			else:
				print("Not connected to network")
				
		# Quit program
		elif command == "Q":
			if NETWORK == 1:
				print("Closing socket...")
				self.closeNetwork()
				
		# Set resolution
		elif command == "R":
			width = int(self.inputParameter("Width"))
			height = int(self.inputParameter("Height"))
			self.setResolution(width, height)
			self.confirmCompletion("Resolution changed")
			
		# Set sharpness
		elif command == "S":
			sharpness = int(self.inputParameter("Sharpness"))
			self.setSharpness(sharpness)
			self.confirmCompletion("Sharpness changed")
			
		# Set saturation
		elif command == "T":
			saturation = int(self.inputParameter("Saturation"))
			self.setSaturation(saturation)
			self.confirmCompletion("Saturation changed")
		
		# Capture stream
		elif command == "V":
			duration = int(self.inputParameter("Duration"))
			filename = self.inputParameter("Filename")
			self.confirmCompletion("Recording started...")
			self.captureStream(duration, fname)
			self.confirmCompletion("Recording finished")
		
		# Change exposure time
		elif command == "X":
			xt = int(self.inputParameter("Exposure time"))
			self.setExposureTime(xt)
			self.confirmCompletion("Exposure time changed")
			
		else:
			print("Not a command")
		
	
	def closeCamera(self):
		'''
		Release the camera resources.
		'''
		
		# Turn off the camera
		if picam == 1:
			self.camera.close()
		
