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


class cameraModuleServer:
	
	def __init__(self):
		'''
		Initialise the server to the Raspberry Pi.
		'''
		
		# Initialise the socket connection
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = socket.gethostbyname(socket.gethostname())
		print(self.host)
		self.server_socket.bind((self.host, 8000))
		self.server_socket.listen(5)
		print("Waiting for Connection...")
		(self.hostSock, self.address) = self.server_socket.accept()
		print("Connection accepted!")
		
		## Accept a single connection
		#self.connection = self.server_socket.accept()[0].makefile('rb')
		
	
	def networkStreamServer(self):
		'''
		Recieve a video stream from the Pi, and playback through VLC.
		'''
		
		# Initialise the socket connection
		#server_socket = socket.socket()
		#server_socket.bind(('0.0.0.0', 8000))
		#server_socket.listen(0)
		
		# Accept a single connection
		connection = server_socket.accept()[0].makefile('rb')
		try:
			# Start stream to VLC
			cmdline = ['vlc', '--demux', 'h264', '-']
			player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
			while True:
				# Send data to VLC input
				data = connection.read(1024)
				if not data:
					break
				player.stdin.write(data)
		finally:
			# Free connection resources
			connection.close()
			#server_socket.close()
			player.terminate()
	
	
	#def networkStreamServer(self):
		#'''
		#Recieve a video stream from the Pi, and playback through VLC.
		#'''
		
		#try:
			## Start stream to VLC
			#cmdline = ['vlc', '--demux', 'h264', '-']
			#player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
			#while True:
				## Send data to VLC input
				#data = self.connection.read(1024)
				#if not data:
					#break
				#player.stdin.write(data)
		#finally:
			## Free connection resources
			#player.terminate()
		
	
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
		
	
	def sendCommand(self):
		'''
		Send a command via terminal to the Raspberry Pi. Command options are:
			"I": Take image and store on Pi
			"V": Record video and store on Pi
			"S": Stream video to host device
			"R": Change camera resolution
			"F": Change camera framerate
			"X": Change camera exposure time
			"Q": Quit
		'''
		
		# List of commands
		opt = ["I","V","S","R","F","X","Q"]
		
		# Initialise socket connection
		#hostSock = socket.socket()
		#hostSock.bind(('0.0.0.0', 8000))
		#hostSock.listen(0)
		
		# Input command from terminal
		command = 0
		while command not in opt:
			command = str(raw_input("Input camera command: ")).upper()
			if command not in opt:
				print("Invalid command")
			else:
				print("Command sent: " + command)
		
		# Send command
		#self.server_socket.send(command)
		self.send_msg(self.hostSock, command)
		
		# Perform command
		if command == "V":
			duration = str(input("Duration: "))
			#self.server_socket.send(duration)
			self.send_msg(self.hostSock, duration)
		elif command == "S":
			duration = str(input("Duration: "))
			#self.server_socket.send(duration)
			self.send_msg(self.hostSock, duration)
			self.networkStreamServer()
		elif command == "R":
			width = str(input("Width: "))
			#self.server_socket.send(width)
			self.send_msg(self.hostSock, width)
			height = str(input("Height: "))
			#self.server_socket.send(height)
			self.send_msg(self.hostSock, height)
			print("Waiting for confirmation")
			print(self.recv_msg(self.hostSock))
		elif command == "F":
			rate = str(input("Framerate: "))
			#self.server_socket.send(rate)
			self.send_msg(self.hostSock, rate)
		elif command == "X":
			speed = str(input("Shutter Speed: "))
			#self.server_socket.send(speed)
			self.send_msg(self.hostSock, speed)
		
		return command
		
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		print("Closing socket...")
		self.server_socket.close()
