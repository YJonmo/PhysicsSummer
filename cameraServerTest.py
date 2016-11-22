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

# Stream from Raspberry Pi to VLC on host computer
camCommand.networkStreamServer()

# Close connection
camCommand.closeServer()
