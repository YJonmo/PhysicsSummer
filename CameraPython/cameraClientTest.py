'''
This script tests the functionallity of the camera client module. This allows 
the camera module of the Raspberry Pi to be controlled remotely via network 
connection.

Author: Damon Hutley
Date: 23rd November 2016
'''

import cameraLibClient
import time

# Initialise the camera module client
camCommand = cameraLibClient.cameraModuleClient()

# Initialise the network
#camCommand.initNetwork()

# Continuously wait for commands from a computer on the network
while True:
	if camCommand.network == 0:
		# Initialise the network
		camCommand.initNetwork()
	else:
		# Process and perform command from network
		command = camCommand.receiveCommand()
		camCommand.performCommand(command)
		
		# Close network if quit command called
		if command == "Q":
			camCommand.closeNetwork()
			time.sleep(5)
	
# Free the camera resources
camCommand.closeCamera()
