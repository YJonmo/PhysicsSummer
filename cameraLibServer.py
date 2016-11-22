'''
Library for the control of the Raspberry Pi camera module from a host computer 
via a network connection.

Author: Damon Hutley
Date: 22nd November 2016
'''


import socket
import subprocess
import time


class cameraModuleServer:
	
	def __init__(self):
		'''
		Initialise the server to the Raspberry Pi.
		'''
		
		# Initialise the socket connection
		
		self.server_socket = socket.socket()
		self.server_socket.bind(('0.0.0.0', 8000))
		self.server_socket.listen(0)
		
		# Accept a single connection
		self.connection = self.server_socket.accept()[0].makefile('rb')
		
	
	#def networkStreamServer(self):
		#'''
		#Recieve a video stream from the Pi, and playback through VLC.
		#'''
		
		## Initialise the socket connection
		#server_socket = socket.socket()
		#server_socket.bind(('0.0.0.0', 8000))
		#server_socket.listen(0)
		
		## Accept a single connection
		#connection = server_socket.accept()[0].makefile('rb')
		#try:
			## Start stream to VLC
			#cmdline = ['vlc', '--demux', 'h264', '-']
			#player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
			#while True:
				## Send data to VLC input
				#data = connection.read(1024)
				#if not data:
					#break
				#player.stdin.write(data)
		#finally:
			## Free connection resources
			#connection.close()
			#server_socket.close()
			#player.terminate()
	
	
	def networkStreamServer(self):
		'''
		Recieve a video stream from the Pi, and playback through VLC.
		'''
		
		try:
			# Start stream to VLC
			cmdline = ['vlc', '--demux', 'h264', '-']
			player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
			while True:
				# Send data to VLC input
				data = self.connection.read(1024)
				if not data:
					break
				player.stdin.write(data)
		finally:
			# Free connection resources
			player.terminate()
		
	
	def sendCommand(self):
		'''
		Send a command via terminal to the Raspberry Pi. Command options are:
			Image: Take image and store on Pi
			Video: Record video and store on Pi
			Stream: Stream video to host device
		'''
		
		# Input command from terminal
		command = input("Input camera command: ")
		
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		self.connection.close()
		self.server_socket.close()
