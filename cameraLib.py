'''
Library for the control of the Raspberry Pi camera module using picamera.

Author: Damon Hutley
Date: 21st November 2016
'''


from io import BytesIO
from picamera import PiCamera
import socket
import subprocess
import time


class cameraModule:
	
	def __init__(self):
		'''
		Initialise the camera module class with picamera.
		'''
		
		# Create an instance of the Picamera class
		self.camera = PiCamera()
		
	
	def capturePhoto(self):
		'''
		Capture a photo and store on Pi.
		'''
		
		# Capture an image and store in file image.png. Will later add options 
		# such as resolution, exposure time, etc.
		self.camera.capture('image.png')
		
	
	def captureStream(self):
		'''
		Capture a video and store on Pi.
		'''
		
	
	def networkStream(self):
		'''
		Stream a video through ethernet and playback through VLC on network computer.
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
		
	
	def remoteControl(self):
		'''
		Control the camera remotely from a network computer.
		'''
		
		
	def closeCamera(self):
		'''
		Release the camera resources.
		'''
		
		self.camera.close()
		
