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


IMAGE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'bmp']


class cameraModuleClient:
	
	def __init__(self):
		'''
		Initialise the server to the Raspberry Pi.
		'''
		
		# Initialise the socket connection
		self.client_socket = socket.socket()
		print("Waiting for connection...")
		self.client_socket.connect(('192.168.1.1', 8000))
		print("Connection accepted")
		
	
	def networkStreamServer(self, duration):
		'''
		Recieve a video stream from the Pi, and playback through VLC.
		'''
		
		# Initialise time
		startTime = time.time()
		
		# Make a file-like object for the connection
		connection = self.client_socket.makefile('rb')
		
		# Start stream to VLC
		cmdline = ['vlc', '--demux', 'h264', '-']
		player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
		while True:#(time.time() - startTime) < duration:
			# Send data to VLC input
			data = connection.read(1024)
			if not data:
				break
			player.stdin.write(data)
		
		# Free connection resources
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
		
	
	def processIntParameter(self, parameter):
		'''
		Wait for parameter from the terminal, and then send integer to the Pi.
		'''
		
		# Receive default, min, max parameters from Pi
		default = int(self.recv_msg(self.client_socket))
		minimum = int(self.recv_msg(self.client_socket))
		maximum = int(self.recv_msg(self.client_socket))
		
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
					if int(value) < minimum:
						print("Value is less than minimum")
					elif int(value) > maximum:
						print("Value is greater than maximum")
					else:
						break
				except ValueError:
					# Condition for parameter inputs that are not integers
					print("Not a number")
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			print("Command failed")
		else:
			print(confirm)
			
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
					print("Image filename must have one of these extensions: " + str(IMAGE_TYPES))
			else:
				# All video extensions supported, so no need to check
				break
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive start confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			print("Command failed")
		else:
			print(confirm)
			
		# Receive finish confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			print("Command failed")
		else:
			print(confirm)
			
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
		print("    Resolution: " + resolution)
		print("    Framerate: " + framerate + " fps")
		print("    Brightness: " + brightness + " %")
		print("    Contrast: " + contrast + " %")
		print("    Analog gain: " + str(float(again)) + " dB")
		print("    Digital gain: " + str(float(dgain)) + " dB")
		print("    Sharpness: " + sharpness + " %")
		print("    Saturation: " + saturation + " %")
		print("    Exposure time: " + xt + " microseconds\n")
		
	
	def receiveFile(self, fname, typ):
		'''
		Receive an image or video from the Pi.
		'''
		
		print("Downloading file...")
		
		# Must have Netcat installed on the command-line
		if typ == "Image":
			os.system("nc 192.168.1.1 60000 > ../../Images/" + fname)
		elif typ == "Video":
			os.system("nc 192.168.1.1 60000 > ../../Videos/" + fname)
		
		print("Downloaded file")
		
	
	def sendCommand(self):
		'''
		Send a command via terminal to the Raspberry Pi.
		'''
		
		# List of commands
		opt = ["B","C","F","G","H","I","N","Q","R","S","T","V","X"]
		
		# Input command from terminal
		command = 0
		while command not in opt:
			command = str(raw_input("Input camera command: ")).upper()
			if command not in opt:
				print("Invalid command")
			else:
				print("Command sent: " + command)
		
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
			print("Note: Gain of 0 automatically sets the gain")
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
			print("Note: Duration of 0 records indefinately, press Esc to exit recording")
			duration = int(self.processIntParameter("Duration (seconds)"))
			self.networkStreamServer(duration)
			
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
			print("Note: Duration of 0 records indefinitely, press Esc to exit recording")
			self.processIntParameter("Duration (seconds)")
			filename = self.processStrParameter("Video filename")
			self.printStats()
			self.receiveFile(filename, "Video")
		
		# Change exposure time
		elif command == "X":
			print("Note: Exposure time of 0 automatically sets the exposure time")
			self.processIntParameter("Exposure time (microseconds)")
		
		return command
		
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		print("Closing socket...")
		self.client_socket.close()
