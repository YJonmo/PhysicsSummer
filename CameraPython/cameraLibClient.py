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
		
		# Accept a single connection
		connection = self.client_socket.makefile('rb')
		
		# Start stream to VLC
		cmdline = ['vlc', '--demux', 'h264', '-']
		player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
		while (time.time() - startTime) < duration:
			# Send data to VLC input
			data = connection.read(1024)
			if not data:
				break
			player.stdin.write(data)
		
		# Free connection resources
		connection.close()
		player.terminate()
		
	
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
			else:
				break # Will add condition to test for correct file type
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			print("Command failed")
		else:
			print(confirm)
			
		# Receive second confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			print("Command failed")
		else:
			print(confirm)
		
	
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
			self.processIntParameter("Framerate")
		
		# Set gain
		elif command == "G":
			self.processIntParameter("Gain")
			
		# Help
		elif command == "H":
			self.printCommands()
			
		# Caputre photo
		elif command == "I":
			self.processStrParameter("Filename")
			# Need to copy image from Pi to client computer
				
		# Network stream
		elif command == "N":
			duration = int(self.processIntParameter("Duration"))
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
			self.processIntParameter("Duration")
			self.processStrParameter("Filename")
			# Need to copy video from Pi to client computer
		
		# Change exposure time
		elif command == "X":
			self.processIntParameter("Exposure time")
		
		return command
		
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		print("Closing socket...")
		self.client_socket.close()
