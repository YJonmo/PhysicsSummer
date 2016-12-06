'''
Library for the control of the Raspberry Pi camera module using picamera.

Author: Damon Hutley
Date: 21st November 2016
'''


from picamera import PiCamera
import socket
import time
import struct
import os
import sys
import datetime


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
FRAMERATE_MIN = 1
FRAMERATE_MAX = 90


class cameraModuleServer:
	
	def __init__(self):
		'''
		Initialise the camera module class with picamera.
		'''
		
		# Create an instance of the Picamera class
		self.camera = PiCamera()
		
		# Initalise network variable
		self.network = 0
		
	
	def setResolution(self, width, height):
		'''
		Set the resolution of the camera.
		'''
		
		# Change the resolution of the camera
		self.camera.resolution = (width, height)
		
	
	def setFrameRate(self, rate):
		'''
		Set the framerate of the camera.
		'''
		
		# Change the framerate of the camera
		self.camera.framerate = rate
		
	
	def setExposureTime(self, speed):
		'''
		Set the exposure time of the camera. Note that the shutter speed 
		must be greater than (1/framerate). A shutter speed of zero will 
		result in an automatically determined exposure time.
		'''
		
		# Change the shutter speed of the camera (in microseconds)
		self.camera.shutter_speed = speed
		
	
	def setSharpness(self, sharpness):
		'''
		Set the sharpness level of the camera. Min: -100, Max: 100.
		'''
		self.camera.sharpness = sharpness
		
	
	def setContrast(self, contrast):
		'''
		Set the contrast level of the camera. Min: -100, Max: 100.
		'''
		self.camera.contrast = contrast
		
	
	def setBrightness(self, brightness):
		'''
		Set the brightness level of the camera. Min: 0, Max: 100.
		'''
		self.camera.brightness = brightness
		
	
	def setSaturation(self, saturation):
		'''
		Set the saturation level of the camera. Min: -100, Max: 100.
		'''
		self.camera.saturation = saturation
		
	
	def setGain(self, gain):
		'''
		Set the gain level of the camera. If ISO is set to zero, then the 
		gain will be chosen automatically. Min: 0, Max: 800.
		'''
		self.camera.iso = gain
		
	
	def capturePhoto(self, fname):
		'''
		Capture a photo and store on Pi.
		'''
		
		# Locate the Images folder
		floc = "../../Images/" + fname
		
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
		
		# Locate the Videos folder
		floc = "../../Videos/" + fname
		
		# Warm up the camera
		self.camera.start_preview()
		time.sleep(2)
		
		# Record the camera for length <duration>, and store in file <fname>
		self.camera.start_recording("../../Videos/input.h264")
		self.camera.wait_recording(duration)
		self.camera.stop_recording()
		self.camera.stop_preview()
		
		# Obtain video stats
		rate = str(self.camera.framerate)
		width = str(self.camera.resolution[0])
		height = str(self.camera.resolution[1])
		
		# Convert raw h264 video into a container to enable playback at the correct framerate
		comStr = "avconv -i ../../Videos/input.h264 -f rawvideo - | avconv -y -f rawvideo -r:v " + rate + " -s:v " + width + "x" + height + " -i - " + floc
		os.system(comStr)
		os.system("rm ../../Videos/input.h264")
		
	
	def networkStreamClient(self, sock, duration):
		'''
		Stream a video through the network.
		'''
		
		if self.network == 1:
			# Create a file-like object for the connection
			connection = sock.makefile('wb')
			try:
				# Warm the camera up
				self.camera.start_preview()
				time.sleep(2)
				
				# Record the camera for length <duration>
				self.camera.start_recording(connection, format = 'h264')
				self.camera.wait_recording(duration)
				self.camera.stop_recording()
				self.camera.stop_preview()
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
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = '192.168.1.1'
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((self.host, 8000))
		self.server_socket.listen(5)
		
		# Wait for a computer to connect
		print("Waiting for connection...")
		(self.hostSock, self.address) = self.server_socket.accept()
		print("Connection accepted")
		self.network = 1
		
	
	def closeNetwork(self):
		'''
		Close the client side network on the Raspberry Pi.
		'''
		
		self.hostSock.close()
		self.server_socket.close()
		self.network = 0
		
	
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
		
		#elif parameter == "Filename":
			#default = "Image" + datetime.datetime.isoformat() + ".png"
			#minimum = None
			#maximum = None
		
		else:
			default = None
		
		if self.network == 1:
			# Send default, min, and max to network computer
			self.send_msg(self.hostSock, str(default))
			self.send_msg(self.hostSock, str(minimum))
			self.send_msg(self.hostSock, str(maximum))
			
			# Wait for parameter input from network computer
			print("Waiting for " + parameter.lower() + "...")
			value = self.recv_msg(self.hostSock)
			print(parameter + ": " + str(value))
		#elif default == None:
		#	# Wait for parameter input from Raspberry Pi terminal
		#	value = str(raw_input(parameter + ": "))
		else:
			# Process parameter inputs from terminal
			while True:
				value = str(raw_input(parameter + " (Default: " + str(default) + ", Min: " + str(minimum) + ", Max: " + str(maximum) + "): "))
				# Set default value if there is no input
				if value == "":
					value = default
					break
				else:
					try:
						# Condition for exceeding min/max bounds
						if int(value) < minimum:
							print("Value is less than minimum")
						elif int(value) > maximum:
							print("Value is greater than maximum")
						else:
							break
					except ValueError:
						# Condition for parameter inputs that are not integers
						print("Not a number")
		
		return value
		
	
	def inputStrParameter(self, parameter):
		'''
		Wait for a parameter from either the network or the Pi terminal.
		'''
		
		if parameter == "Image filename":
			default = "Image" + datetime.datetime.now().isoformat() + ".png"
			
		elif parameter == "Video filename":
			default = "Video" + datetime.datetime.now().isoformat() + ".avi"
		
		else:
			default = None
		
		if self.network == 1:
			# Send default, min, and max to network computer
			self.send_msg(self.hostSock, default)
			
			# Wait for parameter input from network computer
			print("Wating for " + parameter.lower() + "...")
			value = self.recv_msg(self.hostSock)
			print(parameter + ": " + str(value))
		#elif default == None:
		#	# Wait for parameter input from Raspberry Pi terminal
		#	value = str(raw_input(parameter + ": "))
		else:
			# Process parameter inputs from terminal
			while True:
				value = str(raw_input(parameter + " (Default: " + default + "): "))
				# Set default value if there is no input
				if value == "":
					value = default
					break
				else:
					break # Will add condition to test for correct filetype
		
		return value
	
	def confirmCompletion(self, message):
		'''
		Print confirmation message of task completion.
		'''
		
		if self.network == 1:
			self.send_msg(self.hostSock, message)
		else:
			print(message)
		
	
	def printStats(self):
		'''
		Print or send image/video statistics.
		'''
		
		resolution = str(self.camera.resolution[0] + "x" + self.camera.resolution[1])
		framerate = str(self.camera.framerate)
		brightness = str(self.camera.brightness)
		contrast = str(self.camera.contrast)
		gain = str(self.camera.gain)
		sharpness = str(self.camera.sharpness)
		saturation = str(self.camera.saturation)
		xt = str(self.camera.shutter_speed)
		
		if self.network == 1:
			self.send_msg(self.hostSock, resolution)
			self.send_msg(self.hostSock, framerate)
			self.send_msg(self.hostSock, brightness)
			self.send_msg(self.hostSock, contrast)
			self.send_msg(self.hostSock, gain)
			self.send_msg(self.hostSock, sharpness)
			self.send_msg(self.hostSock, saturation)
			self.send_msg(self.hostSock, xt)
		else:
			print("Resolution: " + resolution)
			print("Framerate: " + framerate)
			print("Brightness: " + brightness)
			print("Contrast: " + contrast)
			print("Gain: " + gain)
			print("Sharpness: " + sharpness)
			print("Saturation: " + saturation)
			print("Exposure time: " + xt)
		
	
	def receiveCommand(self):
		'''
		Receive a command from the network or the Pi terminal.
		'''
		
		if self.network == 1:
			# Recieve data from host
			print("Waiting for command...")
			command = self.recv_msg(self.hostSock)
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
			filename = self.inputStrParameter("Image filename")
			self.confirmCompletion("Image capturing...")
			self.capturePhoto(filename)
			self.confirmCompletion("Image captured")
			self.printStats()
				
		# Network stream
		elif command == "N":
			if self.network == 1:
				duration = int(self.inputParameter("Duration"))
				self.networkStreamClient(self.hostSock, duration)
			else:
				print("Not connected to network")
				
		# Quit program
		elif command == "Q":
			if self.network == 1:
				print("Closing socket...")
				self.closeNetwork()
				
		# Set resolution
		elif command == "R":
			width = int(self.inputParameter("Width"))
			self.confirmCompletion("Resolution width changed")
			height = int(self.inputParameter("Height"))
			self.confirmCompletion("Resolution height changed")
			self.setResolution(width, height)
			
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
			self.confirmCompletion("Duration set")
			filename = self.inputStrParameter("Video filename")
			self.confirmCompletion("Recording started...")
			self.captureStream(duration, filename)
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
		self.camera.close()
		
