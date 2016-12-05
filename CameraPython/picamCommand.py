'''
Control of the Raspberry Pi camera module using command input from the terminal.

Author: Damon Hutley
Date: 5th December 2016
'''

import cameraLibClient

# Initialise the camera client module
cam = cameraLibClient.cameraModuleClient()

# Print the list of commands
cam.printCommands()

# Continuously wait for commands from the terminal
while True:
	command = cam.receiveCommand()
	cam.performCommand(command)
	
	# Exit program if quit command called
	if command == "Q":
		break

# Free the camera resources
cam.closeCamera()
