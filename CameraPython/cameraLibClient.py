'''
Library for the control of the Raspberry Pi camera module from a host computer 
via a network connection.

Author: Damon Hutley
Date: 22nd November 2016
'''


import socket
import subprocess
import time
import struct
import os
import sys


IMAGE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'bmp']
COLOUR = True


if COLOUR:
	BLACK = "\033[30m"
	RED = "\033[31m"
	GREEN = "\033[32m"
	YELLOW = "\033[33m"
	BLUE = "\033[34m"
	MAGENTA = "\033[35m"
	CYAN = "\033[36m"
	WHITE = "\033[37m"
	YELLOWFLASH = "\033[33;5m"
	CLEAR = "\033[0m"
else:
	BLACK = "\033[0m"
	RED = "\033[0m"
	GREEN = "\033[0m"
	YELLOW = "\033[0m"
	BLUE = "\033[0m"
	MAGENTA = "\033[0m"
	CYAN = "\033[0m"
	WHITE = "\033[0m"
	YELLOWFLASH = "\033[0m"
	CLEAR = "\033[0m"


class cameraModuleClient:
	
	def __init__(self):
		'''
		Initialise the server to the Raspberry Pi.
		'''
		
		# Initialise the socket connection
		self.client_socket = socket.socket()
		print(YELLOWFLASH + "Waiting for connection..." + CLEAR)
		self.client_socket.connect(('192.168.1.1', 8000))
		print(GREEN + "Connection accepted" + CLEAR)
		
	
	def networkStreamServer(self, duration):
		'''
		Recieve a video stream from the Pi, and playback through VLC.
		'''
		
		# Determine the framerate of the stream
		frate = self.recv_msg(self.client_socket)
		
		# Make a file-like object for the connection
		connection = self.client_socket.makefile('rb')
		
		try:
			# Start stream to VLC
			cmdline = ['vlc', '--demux', 'h264', '--h264-fps', frate, '-']
			player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
			while True:
				# Send data to VLC input
				data = connection.read(1024)
				if not data:
					break
				player.stdin.write(data)
		except KeyboardInterrupt:
			self.send_msg(self.client_socket, "Stop")
			time.sleep(1)
		
		# Free connection resources
		print(GREEN + "Network stream closed" + CLEAR)
		connection.close()
		self.client_socket.close()
		player.terminate()
		self.client_socket = socket.socket()
		self.client_socket.connect(('192.168.1.1', 8000))
		
	
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
		
	
	def printCommands(self):
		'''
		Print a list of commands.
		'''
		
		print("\nList of commands: ")
		print(RED + "    B: Set brightness" + CLEAR)
		print(RED + "    C: Set contrast" + CLEAR)
		print(YELLOW + "    F: Set framerate" + CLEAR)
		print(YELLOW + "    G: Set gain" + CLEAR)
		print(GREEN + "    H: Help" + CLEAR)
		print(GREEN + "    I: Capture an image" + CLEAR)
		print(CYAN + "    N: Stream to network" + CLEAR)
		print(CYAN + "    P: Get camera settings" + CLEAR)
		print(BLUE + "    Q: Quit program" + CLEAR)
		print(BLUE + "    R: Set resolution" + CLEAR)
		print(MAGENTA + "    S: Set sharpness" + CLEAR)
		print(MAGENTA + "    T: Set saturation" + CLEAR)
		print(RED + "    V: Capture a video" + CLEAR)
		print(RED + "    X: Set exposure time\n" + CLEAR)
		
	
	def processIntParameter(self, parameter):
		'''
		Wait for parameter from the terminal, and then send integer to the Pi.
		'''
		
		# Receive default, min, max parameters from Pi
		default = self.recv_msg(self.client_socket)
		minimum = self.recv_msg(self.client_socket)
		maximum = self.recv_msg(self.client_socket)
		
		# Convert default fractions into decimal
		if "/" in default:
			num, den = default.split('/')
			default = str(float(num)/float(den))
		
		# Input parameter value from terminal
		while True:
			value = str(raw_input(parameter + " (Default: " + str(default) + ", Min: " + str(minimum) + ", Max: " + str(maximum) + "): "))
			
			# Set default value if there is no input
			if value == "":
				value = str(default)
				break
			else:
				try:
					# Condition for exceeding min/max bounds
					if float(value) < float(minimum):
						print(RED + "Value is less than minimum" + CLEAR)
					elif float(value) > float(maximum):
						print(RED + "Value is greater than maximum" + CLEAR)
					elif value == "inf":
						value = str(sys.maxint)
						break
					else:
						break
				except ValueError:
					# Condition for parameter inputs that are not integers
					print(RED + "Not a number" + CLEAR)
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			#print("Command failed")
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			print(GREEN + confirm + CLEAR)
			
		return value
		
			
	def processStrParameter(self, parameter):
		'''
		Wait for parameter from the terminal, and then send string to the Pi.
		'''
		
		# Receive default, min, max parameters from Pi
		default = self.recv_msg(self.client_socket)
		
		# Input parameter value from terminal
		while True:
			value = str(raw_input(parameter + " (Default: " + str(default) + "): "))
			
			# Set default value if there is no input
			if value == "":
				value = str(default)
				break
			elif parameter == "Image filename":
				# Check image filename is of correct filetype
				fpart = value.split('.',1)
				
				# Check file has an extension
				if len(fpart) > 1:
					ftype = fpart[-1]
				else:
					ftype = ""
				
				# Continue only if file extension is correct
				if ftype in IMAGE_TYPES:
					break
				else:
					print(RED + "Image filename must have one of these extensions: " + str(IMAGE_TYPES) + CLEAR)
			else:
				# All video extensions supported, so no need to check
				break
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive start confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			#print("Command failed")
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			print(YELLOWFLASH + confirm + CLEAR)
		
		try:
			# Receive finish confirmation message from the Pi.
			confirm = self.recv_msg(self.client_socket)
		except KeyboardInterrupt:
			# Send message to stop recording if Ctrl+C is pressed
			self.send_msg(self.client_socket, "Stop")
			confirm = self.recv_msg(self.client_socket)
		
		if confirm == None:
			#print("Command failed")
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			print(GREEN + confirm + CLEAR)
			
		return value
		
	
	def printStats(self):
		'''
		Receive and print image/video stats after capture.
		'''
		
		# Receive properties of the image/video from the Raspberry Pi
		resolution = self.recv_msg(self.client_socket)
		framerate = self.recv_msg(self.client_socket)
		brightness = self.recv_msg(self.client_socket)
		contrast = self.recv_msg(self.client_socket)
		again = self.recv_msg(self.client_socket)
		dgain = self.recv_msg(self.client_socket)
		sharpness = self.recv_msg(self.client_socket)
		saturation = self.recv_msg(self.client_socket)
		xt = self.recv_msg(self.client_socket)
		
		# Convert gain fractions into decimal
		if "/" in again:
			anum, aden = again.split('/')
			again = str(float(anum)/float(aden))
		
		if "/" in dgain:
			dnum, dden = dgain.split('/')
			dgain = str(float(dnum)/float(dden))
		
		# Convert contrast, sharpness, saturation to percentage
		contrast = str((int(contrast)+100)/2)
		sharpness = str((int(sharpness)+100)/2)
		saturation = str((int(saturation)+100)/2)
		
		# Print the received properties
		print("\nProperties: ")
		print(RED + "    Resolution: " + resolution + CLEAR)
		print(YELLOW + "    Framerate: " + framerate + " fps" + CLEAR)
		print(GREEN + "    Brightness: " + brightness + " %" + CLEAR)
		print(GREEN + "    Contrast: " + contrast + " %" + CLEAR)
		print(CYAN + "    Analog gain: " + str(float(again)) + " dB" + CLEAR)
		print(BLUE + "    Digital gain: " + str(float(dgain)) + " dB" + CLEAR)
		print(BLUE + "    Sharpness: " + sharpness + " %" + CLEAR)
		print(MAGENTA + "    Saturation: " + saturation + " %" + CLEAR)
		print(RED + "    Exposure time: " + xt + " microseconds\n" + CLEAR)
		
	
	def receiveFile(self, fname, typ):
		'''
		Receive an image or video from the Pi.
		'''
		
		print(YELLOWFLASH + "Downloading file..." + CLEAR)
		
		# Must have Netcat installed on the command-line
		if typ == "Image":
			os.system("nc 192.168.1.1 60000 > ../../Images/" + fname)
		elif typ == "Video":
			os.system("nc 192.168.1.1 60000 > ../../Videos/" + fname)
		
		print(GREEN + "Downloaded file" + CLEAR)
		
	
	def sendCommand(self):
		'''
		Send a command via terminal to the Raspberry Pi.
		'''
		
		# List of commands
		opt = ["B","C","F","G","H","I","N","P","Q","R","S","T","V","X"]
		
		# Input command from terminal
		command = 0
		while command not in opt:
			command = str(raw_input("Input camera command: ")).upper()
			if command not in opt:
				print(RED + "Invalid command" + CLEAR)
			else:
				print(GREEN + "Command sent: " + command + CLEAR)
		
		# Send command
		self.send_msg(self.client_socket, command)
		
		# Send parameters and perform command
		# Set brightness
		if command == "B":
			self.processIntParameter("Brightness")
			
		# Set contrast
		elif command == "C":
			self.processIntParameter("Contrast")
			
		# Change framerate
		elif command == "F":
			self.processIntParameter("Framerate (fps)")
		
		# Set gain
		elif command == "G":
			print(CYAN + "Note: Gain of 0 automatically sets the gain" + CLEAR)
			self.processIntParameter("Gain")
			
		# Help
		elif command == "H":
			self.printCommands()
			
		# Caputre photo
		elif command == "I":
			filename = self.processStrParameter("Image filename")
			self.printStats()
			self.receiveFile(filename, "Image")
				
		# Network stream
		elif command == "N":
			print(CYAN + "Note: Press Ctrl+C to exit recording" + CLEAR)
			duration = self.processIntParameter("Duration (seconds)")
			self.networkStreamServer(duration)
		
		# Print camera settings
		elif command == "P":
			self.printStats()
			
		# Change resolution
		elif command == "R":
			self.processIntParameter("Width")
			self.processIntParameter("Height")
				
		# Set sharpness
		elif command == "S":
			self.processIntParameter("Sharpness")
			
		# Set saturation
		elif command == "T":
			self.processIntParameter("Saturation")
		
		# Capture stream
		elif command == "V":
			print(CYAN + "Note: Press Ctrl+C to exit recording" + CLEAR)
			self.processIntParameter("Duration (seconds)")
			filename = self.processStrParameter("Video filename")
			self.printStats()
			self.receiveFile(filename, "Video")
		
		# Change exposure time
		elif command == "X":
			print(CYAN + "Note: Exposure time of 0 automatically sets the exposure time" + CLEAR)
			self.processIntParameter("Exposure time (microseconds)")
		
		return command
		
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		print(YELLOWFLASH + "Closing socket..." + CLEAR)
		self.client_socket.close()
