'''
This script tests the functionallity of the camera client module. This allows 
the camera module of the Raspberry Pi to be controlled remotely via network 
connection.

Author: Damon Hutley
Date: 23rd November 2016
'''

import cameraLibClient

# Initialise the camera module client
camCommand = cameraLibClient.cameraModuleClient()

# Continuously wait for commands from a computer on the network
while True:
	camCommand.receiveCommand()
	
# Free the camera resources
camCommand.closeCamera()
