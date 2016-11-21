'''
Library for the control of the Raspberry Pi camera module using picamera.

Author: Damon Hutley
Date: 21st November 2016
'''


from picamera import PiCamera


class cameraModule:
	
	def __init__(self):
		'''
		Initialise the camera module class with picamera.
		'''
		
		self.camera = PiCamera()
		
	
	def capturePhoto(self):
		'''
		Capture a photo and store on Pi.
		'''
		
	
	def captureStream(self):
		'''
		Capture a video and store on Pi.
		'''
		
	
	def networkStream(self):
		'''
		Stream a video through ethernet and playback through VLC on network computer.
		'''
		
	
	def remoteControl(self):
		'''
		Control the camera remotely from a network computer.
		'''
		
