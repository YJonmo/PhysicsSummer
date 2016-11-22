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
		self.server_socket = socket.socket()
		self.server_socket.bind(('0.0.0.0', 8000))
		self.server_socket.listen(0)
		
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
		
	
	def send_msg(sock, msg):
		'''
		Send message with a prefixed length.
		'''
		
		# Prefix each message with a 4-byte length (network byte order)
		msg = struct.pack('>I', len(msg)) + msg
		sock.sendall(msg)
		
	
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
		
		# Send command
		#self.server_socket.send(command)
		send_msg(self.server_socket, command)
		
		# Perform command
		if command == "V":
			duration = input("Duration: ")
			#self.server_socket.send(duration)
			send_msg(self.server_socket, duration)
		elif command == "S":
			duration = input("Duration: ")
			#self.server_socket.send(duration)
			send_msg(self.server_socket, duration)
			self.networkStreamServer()
		elif command == "R":
			width = input("Width: ")
			#self.server_socket.send(width)
			send_msg(self.server_socket, width)
			height = input("Height: ")
			#self.server_socket.send(height)
			send_msg(self.server_socket, height)
		elif command == "F":
			rate = input("Framerate: ")
			#self.server_socket.send(rate)
			send_msg(self.server_socket, rate)
		elif command == "X":
			speed = input("Shutter Speed: ")
			#self.server_socket.send(speed)
			send_msg(self.server_socket, speed)
		
		return command
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		self.server_socket.close()
