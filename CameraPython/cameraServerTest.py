'''
This script tests the functionallity of the camera server module. This allows 
the camera module of the Raspberry Pi to be controlled remotely via network 
connection.

Author: Damon Hutley
Date: 23rd November 2016
'''

import cameraLibServer
import time
import sys

# Initialise the camera module client
camCommand = cameraLibServer.cameraModuleServer()

# Continuously wait for commands from a computer on the network
while True:
	if camCommand.network == 0:
		# Initialise the network
		camCommand.initNetwork()
	else:
		try:
		# Process and perform command from network
			command = camCommand.receiveCommand()
			camCommand.performCommand(command)
		except:
			e = sys.exc_info()[0]
			print("Error: %s" % e)
			time.sleep(1)
			camCommand.closeNetwork()
		
		# Close network if quit command called
		if command == "Q":
			time.sleep(1)
			camCommand.closeNetwork()
	
# Free the camera resources
camCommand.closeCamera()
