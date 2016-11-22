'''
This script tests the functionallity of the camera server module. This allows 
the camera module of the Raspberry Pi to be controlled remotely via network 
connection.

Author: Damon Hutley
Date: 22nd November 2016
'''

import cameraLibServer

# Initialise the camera module server
camCommand = cameraLibServer.cameraModuleServer()

# Continuously ask for commands to send to the Raspberry Pi from the terminal.
while True:
	command = camCommand.sendCommand()
	
	# Exit program if quit command called
	if command = "Q":
		break

## Stream from Raspberry Pi to VLC on host computer
#camCommand.networkStreamServer()

# Close connection
camCommand.closeServer()
