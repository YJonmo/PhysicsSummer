'''
This script tests the functionallity of the camera server module. This allows 
the camera module of the Raspberry Pi to be controlled remotely via network 
connection.

Author: Damon Hutley
Date: 23rd November 2016
'''

import cameraLibServer
import picamera
from multiprocessing import Process
import time
import sys
import subprocess

#def cmdProcess():
	## Initialise the camera module client
	#camCommand = cameraLibServer.cameraModuleServer()

	## Continuously wait for commands from a computer on the network
	#while True:
		#if camCommand.network == 0:
			## Initialise the network
			#camCommand.initNetwork()
			
			## Initialise socket checking process
			##errSock = Process(target = camCommand.errorChk)
			##errSock.start()
		#else:
			#try:
				## Process and perform command from network
				#command = camCommand.receiveCommand()
				#camCommand.performCommand(command)
				
				## Close network if quit command called
				#if command == "Q":# or not errSock.is_alive():
					##errSock.terminate()
					#time.sleep(1)
					#camCommand.closeNetwork()
			
			#except:
				#e = sys.exc_info()[0]
				#print("Error: %s" % e)
				##errSock.terminate()
				#camCommand.camera.stop_preview()
				#time.sleep(1)
				#camCommand.closeNetwork()
				
	## Free the camera resources
	#print("Closing camera...")
	#camCommand.closeCamera()

#def errChk():
	#'''
	#Process to check for a drop in the socket connection.
	#'''
	#while True:
		##ready_to_read, ready_to_write, in_error = select.select([self.hostSock,], [self.hostSock,], [], 5)
		##response = os.system("ping -c 1 192.168.1.7")
		#response = subprocess.Popen(['ping','-c','1','192.168.1.7'], stdout = subprocess.PIPE).communicate()[0]
		##print(response)
		#if "0 received" in response:
			#raise Exception("LostConnection")
		#time.sleep(1)

#cflag = 0

#try:
	#while True:
		#if cflag == 0:
			## Initialise socket error checking and command performing tasks
			#errSock = Process(target = errChk)
			#cmdSock = Process(target = cmdProcess)
			
			#errSock.start()
			#cmdSock.start()
			
			#cflag = 1
		
		#elif not errSock.is_alive() or not cmdSock.is_alive():
			## Terminate processes and restart network if an exception occurs
			#errSock.terminate()
			#cmdSock.terminate()
			##camCommand.camera.stop_preview()
			##time.sleep(1)
			##camCommand.closeNetwork()
			
			#cflag = 0
#finally:
	## Terminate processes and close network
	#errSock.terminate()
	#cmdSock.terminate()
	##camCommand.camera.stop_preview()
	##time.sleep(1)
	##camCommand.closeNetwork()

	## Free the camera resources
	##print("Closing camera...")
	##camCommand.closeCamera()

# Initialise the camera module client
camCommand = cameraLibServer.cameraModuleServer()

# Continuously wait for commands from a computer on the network
while True:
	if camCommand.network == 0:
		# Initialise the network
		camCommand.initNetwork()
		
		# Initialise socket checking process
		#errSock = Process(target = camCommand.errorChk)
		#errSock.start()
	else:
		try:
			# Process and perform command from network
			command = camCommand.receiveCommand()
			camCommand.performCommand(command)
			
			# Close network if quit command called
			if command == "Q":# or not errSock.is_alive():
				#errSock.terminate()
				time.sleep(1)
				camCommand.closeNetwork()
		
		except picamera.exc.PiCameraAlreadyRecording:
			camCommand.closeCamera()
			camCommand.__init__()
			
		except:
			e = sys.exc_info()[0]
			print("Error: %s" % e)
			#errSock.terminate()
			camCommand.camera.stop_preview()
			time.sleep(1)
			camCommand.closeNetwork()
			
# Free the camera resources
print("Closing camera...")
camCommand.closeCamera()

#try:
	#while True:
		#if camCommand.network == 0:
			## Initialise the network
			#camCommand.initNetwork()
			
			## Initialise socket error checking and command performing tasks
			#errSock = Process(target = camCommand.errorChk)
			#cmdSock = Process(target = camCommand.cmdRun)
			
			#errSock.start()
			#cmdSock.start()
		
		#elif not errSock.is_alive() or not cmdSock.is_alive():
			## Terminate processes and restart network if an exception occurs
			#errSock.terminate()
			#cmdSock.terminate()
			##camCommand.camera.stop_preview()
			#time.sleep(1)
			#camCommand.closeNetwork()
#finally:
	## Terminate processes and close network
	#errSock.terminate()
	#cmdSock.terminate()
	##camCommand.camera.stop_preview()
	#time.sleep(1)
	#camCommand.closeNetwork()

	## Free the camera resources
	#print("Closing camera...")
	#camCommand.closeCamera()
