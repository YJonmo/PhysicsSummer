'''
Library for the control of the Raspberry Pi camera module from a host computer 
via a network connection.

Author: Damon Hutley
Date: 22nd November 2016
'''


from io import BytesIO
import socket
import subprocess
import time


class cameraModuleServer:
	
	def __init__(self):
		'''
		Initialise the camera module class with picamera.
		'''
		
		# Will probably initialise the socket connection here
		pass
		
	
	def networkStreamServer(self):
		'''
		Recieve a video stream from the Pi, and playback through VLC.
		'''
		
		# Initialise the socket connection
		server_socket = socket.socket()
		server_socket.bind(('0.0.0.0', 8000))
		server_socket.listen(0)
		
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
			server_socket.close()
			player.terminate()
		
	
	def remoteControlServer(self):
		'''
		Control the camera remotely from a network computer.
		'''
		
