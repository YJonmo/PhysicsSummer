'''
This script tests the functionallity of the camera server module. This allows 
the camera module of the Raspberry Pi to be controlled remotely via network 
connection.

Author: Damon Hutley
Date: 23rd November 2016
'''

import cameraLibServer
from multiprocessing import Process
import time
import sys

# Initialise the camera module client
camCommand = cameraLibServer.cameraModuleServer()

# Continuously wait for commands from a computer on the network
while True:
	if camCommand.network == 0:
		# Initialise the network
		camCommand.initNetwork()
		
		# Initialise socket checking process
		errSock = Process(target = camCommand.errorChk)
		errSock.start()
	else:
		try:
			# Process and perform command from network
			command = camCommand.receiveCommand()
			camCommand.performCommand(command)
			
			# Close network if quit command called
			if command == "Q" or not errSock.is_alive():
				time.sleep(1)
				camCommand.closeNetwork()
				errSock.terminate()
		
		except:
			e = sys.exc_info()[0]
			print("Error: %s" % e)
			camCommand.camera.stop_preview()
			time.sleep(1)
			camCommand.closeNetwork()
			errSock.terminate()
		
# Free the camera resources (will never reach here though (will change))
camCommand.closeCamera()
