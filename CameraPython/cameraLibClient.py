'''
Library for the control of the Raspberry Pi camera module from a host computer 
via a network connection.

Author: Damon Hutley
Date: 22nd November 2016
'''


import socket
import subprocess
import time
import struct
import os
import sys
import tempfile
from multiprocessing import Process, Value
from Tkinter import Tk, Text, BOTH, W, N, E, S, RAISED, Frame, LEFT, TOP, BOTTOM, DISABLED, NORMAL
from ttk import Button, Style, Label, Entry


IMAGE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'bmp']
COLOUR = True


if COLOUR:
	BLACK = "\033[30m"
	RED = "\033[31m"
	GREEN = "\033[32m"
	YELLOW = "\033[33m"
	BLUE = "\033[34m"
	MAGENTA = "\033[35m"
	CYAN = "\033[36m"
	WHITE = "\033[37m"
	YELLOWFLASH = "\033[33;5m"
	CLEAR = "\033[0m"
else:
	BLACK = "\033[0m"
	RED = "\033[0m"
	GREEN = "\033[0m"
	YELLOW = "\033[0m"
	BLUE = "\033[0m"
	MAGENTA = "\033[0m"
	CYAN = "\033[0m"
	WHITE = "\033[0m"
	YELLOWFLASH = "\033[0m"
	CLEAR = "\033[0m"


class cameraGUI(Frame):
	
	def __init__(self, parent, camera):
		# Initialise the GUI to control the Raspberry Pi camera
		Frame.__init__(self, parent)
		self.parent = parent
		self.camera = camera
		self.buttonWidth = 20
		self.initUI()
		
		# Initialise global values to store Entry text.
		self.fnameValue = 0
		self.durValue = 0
		self.error = 0
	
	def initUI(self):
		'''
		Completely setup and display the camera GUI. This is run once at 
		initialisation of the camera GUI module.
		'''
		
		# Initialise the UI
		self.parent.title("Raspberry Pi Camera")
		self.style = Style()
		self.style.theme_use("clam")
		
		# Determine column values
		pcolumn = 1
		ctcolumn = 2
		ccolumn = 3
		bcolumn = 0
		mintcolumn = 4
		mincolumn = 5
		maxtcolumn = 6
		maxcolumn = 7
		
		# Split the GUI into 3 sections
		self.frame = Frame(self, relief=RAISED, borderwidth=1, width=100, height=480)
		self.frame.pack(side=LEFT, expand=0, fill=BOTH)
		
		self.frame2 = Frame(self, relief=RAISED, borderwidth=1, width=540, height=120)
		self.frame2.pack(side=TOP, expand=0, fill=BOTH)
		
		self.frame3 = Frame(self, relief=RAISED, borderwidth=1, width=540, height=360)
		self.frame3.pack(side=TOP, expand=0, fill=BOTH)
		
		self.pack(fill=BOTH, expand=1)
		
		# Set the buttons corresponding to camera commands
		lbl = Label(self.frame, text="Commands")
		lbl.grid(row=0, column=0, pady=4, padx=5)
		
		self.imageButton = Button(self.frame, text="Take Image", command= lambda: self.dispChange("I"), width=self.buttonWidth)
		self.imageButton.grid(row=1, column=bcolumn, pady=4)
		
		self.videoButton = Button(self.frame, text="Take Video", command= lambda: self.dispChange("V"), width=self.buttonWidth)
		self.videoButton.grid(row=2, column=bcolumn, pady=4)
		
		self.networkButton = Button(self.frame, text="Stream to VLC", command= lambda: self.dispChange("N"), width=self.buttonWidth)
		self.networkButton.grid(row=3, column=bcolumn, pady=4)
		
		self.isButton = Button(self.frame, text="Image Subtraction", command= lambda: self.dispChange("O"), width=self.buttonWidth)
		self.isButton.grid(row=4, column=bcolumn, pady=4)
		
		self.resButton = Button(self.frame, text="Set Resolution", command= lambda: self.dispChange("R"), width=self.buttonWidth)
		self.resButton.grid(row=5, column=bcolumn, pady=4)
		
		self.frButton = Button(self.frame, text="Set Framerate", command= lambda: self.dispChange("F"), width=self.buttonWidth)
		self.frButton.grid(row=6, column=bcolumn, pady=4)
		
		self.xtButton = Button(self.frame, text="Set Exposure Time", command= lambda: self.dispChange("X"), width=self.buttonWidth)
		self.xtButton.grid(row=7, column=bcolumn, pady=4)
		
		self.brButton = Button(self.frame, text="Set Brightness", command= lambda: self.dispChange("B"), width=self.buttonWidth)
		self.brButton.grid(row=8, column=bcolumn, pady=4)
		
		self.coButton = Button(self.frame, text="Set Contrast", command= lambda: self.dispChange("C"), width=self.buttonWidth)
		self.coButton.grid(row=9, column=bcolumn, pady=4)
		
		self.gnButton = Button(self.frame, text="Set ISO", command= lambda: self.dispChange("G"), width=self.buttonWidth)
		self.gnButton.grid(row=10, column=bcolumn, pady=4)
		
		self.stButton = Button(self.frame, text="Set Saturation", command= lambda: self.dispChange("U"), width=self.buttonWidth)
		self.stButton.grid(row=11, column=bcolumn, pady=4)
		
		self.shButton = Button(self.frame, text="Set Sharpness", command= lambda: self.dispChange("S"), width=self.buttonWidth)
		self.shButton.grid(row=12, column=bcolumn, pady=4)
		
		self.quitButton = Button(self.frame, text="Quit", command= lambda: self.camera.quitGUI(self), width=self.buttonWidth)
		self.quitButton.grid(row=13, column=bcolumn, pady=4)
		
		# Set the section to control a mode
		ctrlbl = Label(self.frame2, text="Control")
		ctrlbl.grid(sticky=W, row=0, column=0, columnspan=2, pady=(5,10), padx=5)
		
		self.modelb = Label(self.frame2, text="Mode: Waiting    ")
		self.modelb.grid(sticky=W, row=1, column=0, columnspan=2, pady=(4,10), padx=5)
		
		self.statlb = Label(self.frame2, text="Status: Connected to Raspberry Pi")
		self.statlb.grid(sticky=W, row=1, column=2, columnspan=7, pady=(4,10), padx=5)
		
		self.but = Button(self.frame2)
		self.but2 = Button(self.frame2)
		self.txt = Entry(self.frame2)
		self.txt2 = Entry(self.frame2)
		
		self.lbl = Label(self.frame2, text=" ")
		self.lbl.grid(sticky=W, row=2, column=1, pady=10, padx=5)
		
		self.lbl2 = Label(self.frame2, text=" ")
		self.lbl2.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
		
		# Receive the camera properties from the Raspberry Pi
		self.camera.sendCommand("A")
		stats = self.camera.receiveAll()
		
		# Set the section containing the current camera properties
		titlbl = Label(self.frame3, text="Properties")
		titlbl.grid(sticky=W, row=4, column=pcolumn, pady=(8,10), padx=5)
		
		reswlbl = Label(self.frame3, text="Width: ")
		reswlbl.grid(sticky=W, row=5, column=pcolumn, pady=10, padx=5)
		
		reshlbl = Label(self.frame3, text="Height: ")
		reshlbl.grid(sticky=W, row=6, column=pcolumn, pady=10, padx=5)
		
		frlbl = Label(self.frame3, text="Framerate (fps): ")
		frlbl.grid(sticky=W, row=7, column=pcolumn, pady=10, padx=5)
		
		xtlbl = Label(self.frame3, text=u'Exposure Time (\u03bcs): ')
		xtlbl.grid(sticky=W, row=8, column=pcolumn, pady=10, padx=5)
		
		brlbl = Label(self.frame3, text="Brightness: ")
		brlbl.grid(sticky=W, row=9, column=pcolumn, pady=10, padx=5)
		
		colbl = Label(self.frame3, text="Contrast: ")
		colbl.grid(sticky=W, row=10, column=pcolumn, pady=10, padx=5)
		
		gnlbl = Label(self.frame3, text="ISO: ")
		gnlbl.grid(sticky=W, row=11, column=pcolumn, pady=10, padx=5)
		
		stlbl = Label(self.frame3, text="Saturation: ")
		stlbl.grid(sticky=W, row=12, column=pcolumn, pady=10, padx=5)
		
		stlbl = Label(self.frame3, text="Sharpness: ")
		stlbl.grid(sticky=W, row=13, column=pcolumn, pady=10, padx=5)
		
		self.proplab = []
		self.minplab = []
		self.maxplab = []
		propwidth = 6
		
		# Set the actual camera properties
		for i in range(27):
			if i % 3 == 0:
				currlab = Label(self.frame3, text="Curr:", width=propwidth)
				currlab.grid(sticky=W, row=(5+i/3), column=ctcolumn, pady=4, padx=2)
				
				self.proplab.append(Label(self.frame3, text=str(stats[i]), width=propwidth))
				self.proplab[i/3].grid(sticky=W, row=(5+i/3), column=ccolumn, pady=4, padx=5)
			
			if i % 3 == 1:
				minlab = Label(self.frame3, text="Min:", width=propwidth)
				minlab.grid(sticky=W, row=(5+i/3), column=mintcolumn, pady=4, padx=2)
				
				self.minplab.append(Label(self.frame3, text=str(stats[i]), width=propwidth))
				self.minplab[i/3].grid(sticky=W, row=(5+i/3), column=mincolumn, pady=4, padx=5)
			
			if i % 3 == 2:
				maxlab = Label(self.frame3, text="Max:", width=propwidth)
				maxlab.grid(sticky=W, row=(5+i/3), column=maxtcolumn, pady=4, padx=2)
				
				self.maxplab.append(Label(self.frame3, text=str(stats[i]), width=propwidth))
				self.maxplab[i/3].grid(sticky=W, row=(5+i/3), column=maxcolumn, pady=4, padx=5)
		
	
	def dispProps(self):
		'''
		Display updated properties of the camera module on the GUI.
		'''
		
		# Receive the values of all camera properties
		self.camera.sendCommand("A")
		stats = self.camera.receiveAll()
		
		# Update every property
		for i in range(27):
			if i % 3 == 0:
				self.proplab[i/3].config(text=str(stats[i]))
			
			if i % 3 == 1:
				self.minplab[i/3].config(text=str(stats[i]))
			
			if i % 3 == 2:
				self.maxplab[i/3].config(text=str(stats[i]))
		
	
	def dispChange(self, useCmd):
		'''
		Change the control section of the GUI if there is a mode change.
		'''
		
		self.but.grid_forget()
		self.but2.grid_forget()
		self.lbl.grid_forget()
		self.lbl2.grid_forget()
		self.txt.grid_forget()
		self.txt2.grid_forget()
		
		if useCmd == "I":
			self.modelb.config(text="Mode: Image      ")
			
			self.but = Button(self.frame2, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text="Enter Filename:  ")
			self.lbl.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt = Entry(self.frame2)
			self.txt.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.lbl2 = Label(self.frame2, text=" ")
			self.lbl2.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
		elif useCmd == "V":
			self.modelb.config(text="Mode: Video      ")
			
			self.lbl = Label(self.frame2, text="Enter Filename:  ")
			self.lbl.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt = Entry(self.frame2)
			self.txt.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.lbl2 = Label(self.frame2, text="Enter Duration:  ")
			self.lbl2.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=3, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth/2)
			self.but.grid(sticky=W, row=3, column=5, pady=0, padx=2.5)
			
			self.but2 = Button(self.frame2, text="Stop", state=DISABLED, command= lambda: self.streamStop(useCmd), width=self.buttonWidth/2)
			self.but2.grid(sticky=W, row=3, column=6, pady=0, padx=2.5)
			
		elif useCmd == "N":
			self.modelb.config(text="Mode: Stream     ")
			
			self.lbl2 = Label(self.frame2, text="Enter Duration:  ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth/2)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=2.5)
			
			self.but2 = Button(self.frame2, text="Stop", state=DISABLED, command= lambda: self.streamStop(useCmd), width=self.buttonWidth/2)
			self.but2.grid(sticky=W, row=2, column=6, pady=4, padx=2.5)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
		elif useCmd == "O":
			self.modelb.config(text="Mode: Subtract   ")
			
			self.lbl2 = Label(self.frame2, text="Enter Duration:  ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth/2)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=2.5)
			
			self.but2 = Button(self.frame2, text="Stop", state=DISABLED, command= lambda: self.streamStop(useCmd), width=self.buttonWidth/2)
			self.but2.grid(sticky=W, row=2, column=6, pady=4, padx=2.5)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
		elif useCmd == "R":
			self.modelb.config(text="Mode: Resolution ")
		
			self.lbl2 = Label(self.frame2, text="Enter Width:     ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text="Enter Height:    ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
			self.txt = Entry(self.frame2)
			self.txt.grid(sticky=W, row=3, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=3, column=5, pady=0, padx=5, columnspan=3)
		
		elif useCmd == "F":
			self.modelb.config(text="Mode: Framerate  ")
		
			self.lbl2 = Label(self.frame2, text="Enter Rate (fps):")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
		
		elif useCmd == "X":
			self.modelb.config(text="Mode: Exposure   ")
		
			self.lbl2 = Label(self.frame2, text=u'Enter Time (\u03bcs):')
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
		
		elif useCmd == "B":
			self.modelb.config(text="Mode: Brightness ")
		
			self.lbl2 = Label(self.frame2, text="Enter Brightness:")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
		
		elif useCmd == "C":
			self.modelb.config(text="Mode: Contrast   ")
		
			self.lbl2 = Label(self.frame2, text="Enter Contrast:  ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
		elif useCmd == "G":
			self.modelb.config(text="Mode: Gain       ")
		
			self.lbl2 = Label(self.frame2, text="Enter Gain:      ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
		elif useCmd == "U":
			self.modelb.config(text="Mode: Saturation ")
		
			self.lbl2 = Label(self.frame2, text="Enter Saturation:")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
			
		elif useCmd == "S":
			self.modelb.config(text="Mode: Sharpness  ")
		
			self.lbl2 = Label(self.frame2, text="Enter Sharpness: ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=10, padx=5)
			
			self.txt2 = Entry(self.frame2)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5, columnspan=3)
			
			self.but = Button(self.frame2, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=5, pady=4, padx=5, columnspan=3)
			
			self.lbl = Label(self.frame2, text=" ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=(10,9), padx=5)
	
	
	def retStr(self, useCmd):
		'''
		Determine the parameters in the Entry text boxes, and start 
		running the command.
		'''
		
		self.fnameValue = self.txt.get()
		self.durValue = self.txt2.get()

		self.camera.sendCommand(useCmd)
		
		if self.camera.durStop == "inf":
			self.imageButton.config(state=DISABLED)
			self.videoButton.config(state=DISABLED)
			self.networkButton.config(state=DISABLED)
			self.isButton.config(state=DISABLED)
			self.resButton.config(state=DISABLED)
			self.frButton.config(state=DISABLED)
			self.xtButton.config(state=DISABLED)
			self.brButton.config(state=DISABLED)
			self.coButton.config(state=DISABLED)
			self.gnButton.config(state=DISABLED)
			self.stButton.config(state=DISABLED)
			self.shButton.config(state=DISABLED)
			self.quitButton.config(state=DISABLED)
			self.but.config(state=DISABLED)
			self.but2.config(state=NORMAL)
	
	
	def streamStop(self, useCmd):
		'''
		Process that is run if the stop button is pressed.
		'''
		
		# Set the value to stop the stream/record process
		self.camera.procStop.value = 1
		time.sleep(1)
		
		self.imageButton.config(state=NORMAL)
		self.videoButton.config(state=NORMAL)
		self.networkButton.config(state=NORMAL)
		self.isButton.config(state=NORMAL)
		self.resButton.config(state=NORMAL)
		self.frButton.config(state=NORMAL)
		self.xtButton.config(state=NORMAL)
		self.brButton.config(state=NORMAL)
		self.coButton.config(state=NORMAL)
		self.gnButton.config(state=NORMAL)
		self.stButton.config(state=NORMAL)
		self.shButton.config(state=NORMAL)
		self.quitButton.config(state=NORMAL)
		self.but.config(state=NORMAL)
		self.but2.config(state=DISABLED)
		
		if useCmd == "N":
			# Free connection resources
			print(GREEN + "Network stream closed" + CLEAR)
			self.camera.client_socket.close()
			self.camera.client_socket = socket.socket()
			self.camera.client_socket.connect(('192.168.1.1', 8000))
		elif useCmd == "V":
			# Receive the video file
			self.statlb.config(text="Status: " + self.camera.confStop)
			Tk.update(self.camera.root)
			self.camera.printStats()
			self.camera.receiveFile(self.camera.fileStop, "Video")


class cameraModuleClient:
	
	def __init__(self):
		'''
		Initialise the server to the Raspberry Pi.
		'''
		
		# Initialise the socket connection
		self.client_socket = socket.socket()
		print(YELLOW + "Waiting for connection..." + CLEAR)
		self.client_socket.connect(('192.168.1.1', 8000))
		print(GREEN + "Connection accepted" + CLEAR)
		
		# GUI settings
		self.useGUI = 0
		self.procStop = Value('i', 0)
		self.durStop = 0
		self.fileStop = ""
		self.confStop = ""
		self.msgSent = 0
		
	
	def networkStreamServer(self, duration):
		'''
		Recieve a video stream from the Pi, and playback through VLC.
		'''
		
		# Determine the framerate of the stream
		frate = self.recv_msg(self.client_socket)
		self.msgSent = 0
		
		# Make a file-like object for the connection
		connection = self.client_socket.makefile('rb')

		try:
			# Start stream to VLC
			cmdline = ['vlc', '--demux', 'h264', '--h264-fps', frate, '-']
			player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
			while True:
				# Send data to VLC input
				data = connection.read(1024)
				if not data:
					break
				player.stdin.write(data)
				
				# Finish if stop button is pressed
				if self.useGUI == 1 and self.procStop.value == 1 and self.durStop == "inf":
					raise KeyboardInterrupt
			
		except KeyboardInterrupt:
			self.send_msg(self.client_socket, "Stop")
			self.msgSent = 1
			time.sleep(1)
		
		# Close resources
		connection.close()
		player.terminate()
		
		if not self.useGUI == 1 or not self.durStop == "inf":
			# Free connection resources
			print(GREEN + "Network stream closed" + CLEAR)
			self.client_socket.close()
			self.client_socket = socket.socket()
			self.client_socket.connect(('192.168.1.1', 8000))
	
	
	def networkStreamSubtract(self, duration):
		'''
		Recieve a video stream from the Pi, and perform image subtraction through openCV.
		'''
		
		# Determine the framerate of the stream
		frate = self.recv_msg(self.client_socket)
		
		try:
			# Receive a stream from gstreamer, and pipe into the openCV executable.
			gstcmd = "tcpclientsrc host=192.168.1.1 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, framerate=" + frate + "/1 ! avdec_h264 ! videoconvert ! queue max-size-buffers=0 max-size-time=0 max-size-bytes=0 ! appsink"
			#gstcmd = "tcpclientsrc host=192.168.1.1 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, framerate=" + frate + "/1 ! avdec_h264 ! videoconvert ! appsink"
			subline = ['./BackGroundSubbThread', '-vid', gstcmd]#, '-back', '../../Images/B3.jpg']
			time.sleep(0.1)
			player = subprocess.Popen(subline, preexec_fn=os.setpgrp)
			
			if self.useGUI == 1 and self.durStop == "inf":
				# Stop when stop button is pressed or process has ended
				while player.poll() == None:
					if self.procStop.value == 1:
						raise KeyboardInterrupt

			else:
				# Wait for executable to exit
				player.wait()
		
		except KeyboardInterrupt:
			# Free resources
			#print(GREEN + "Network stream closed" + CLEAR)
			#player.terminate()

			self.send_msg(self.client_socket, "Stop")
			#time.sleep(1)
			player.wait()
		
	
	def send_msg(self, sock, msg):
		'''
		Send message with a prefixed length.
		'''
		
		# Prefix each message with a 4-byte length (network byte order)
		msg = struct.pack('>I', len(msg)) + msg
		sock.sendall(msg)
		
	
	def recv_msg(self, sock):
		'''
		Receive a message from the network.
		'''
		
		# Read message length and unpack it into an integer
		raw_msglen = self.recvall(sock, 4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		
		# Read the message data
		return self.recvall(sock, msglen)
		
	
	def recvall(self, sock, n):
		'''
		Decode the message given the message length.
		'''
		
		# Helper function to recv n bytes or return None if EOF is hit
		data = ''
		while len(data) < n:
			packet = sock.recv(n - len(data))
			if not packet:
				return None
			data += packet
		
		return data
		
	
	def printCommands(self):
		'''
		Print a list of commands.
		'''
		
		print("\nList of commands: ")
		print("    B: Set brightness")
		print("    C: Set contrast")
		print("    F: Set framerate")
		print("    G: Set gain")
		print("    H: Help")
		print("    I: Capture an image")
		print("    N: Stream to network")
		print("    O: Stream with image subtraction")
		print("    P: Get camera settings")
		print("    Q: Quit program")
		print("    R: Set resolution")
		print("    S: Set sharpness")
		print("    T: Capture with trigger")
		print("    U: Set saturation")
		print("    V: Capture a video")
		print("    X: Set exposure time\n")
		
		
	def receiveAll(self):
		'''
		Receive all camera properties for use by the GUI.
		'''
		
		result = []
		
		# Fetch all camera properties, including mins and maxs
		for i in range(27):
			result.append(self.recv_msg(self.client_socket))
		
		return result
	
	
	def processIntParameter(self, parameter):
		'''
		Wait for parameter from the terminal, and then send integer to the Pi.
		'''
		
		# Receive default, min, max parameters from Pi
		default = self.recv_msg(self.client_socket)
		minimum = self.recv_msg(self.client_socket)
		maximum = self.recv_msg(self.client_socket)
		
		# Convert default fractions into decimal
		if "/" in default:
			num, den = default.split('/')
			default = str(float(num)/float(den))
		
		# Input parameter value from terminal or GUI
		while True:
			if self.useGUI == 1:
				value = self.app.durValue
			else:
				value = str(raw_input(parameter + " (Default: " + str(default) + ", Min: " + str(minimum) + ", Max: " + str(maximum) + "): "))
			
			# Set default value if there is no input
			if value == "":
				value = str(default)
				break
			else:
				try:
					# Condition for exceeding min/max bounds
					if float(value) < float(minimum):
						if self.useGUI == 1:
							self.app.statlb.config(text="Status: Value is less than minimum")
							Tk.update(self.root)
							value = default
							self.app.error = 1
							break
						else:
							print(RED + "Value is less than minimum" + CLEAR)
					elif float(value) > float(maximum):
						if self.useGUI == 1:
							self.app.statlb.config(text="Status: Value is greater than maximum")
							Tk.update(self.root)
							value = default
							self.app.error = 1
							break
						else:
							print(RED + "Value is greater than maximum" + CLEAR)
					elif value == "inf":
						value = str(sys.maxint)
						break
					else:
						break
				except ValueError:
					# Condition for parameter inputs that are not integers
					if self.useGUI == 1:
						self.app.statlb.config(text="Status: Not a number")
						Tk.update(self.root)
						value = default
						self.app.error = 1
						break
					else:
						print(RED + "Not a number" + CLEAR)
		
		# Save duration value to global if GUI is used
		if self.useGUI == 1 and parameter == "Duration (seconds)":
			self.durStop = value
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			if self.useGUI == 1 and self.app.error == 0:
				if "Resolution" in confirm:
					confirm = "Resolution changed"
				self.app.statlb.config(text="Status: " + confirm)
				Tk.update(self.root)
			elif self.useGUI == 1 and self.app.error == 1:
				self.app.error = 0
			else:
				print(GREEN + confirm + CLEAR)
			
		return value
		
			
	def processStrParameter(self, parameter):
		'''
		Wait for parameter from the terminal, and then send string to the Pi.
		'''
		
		# Receive default, min, max parameters from Pi
		default = self.recv_msg(self.client_socket)

		# Input parameter value from terminal or GUI
		while True:
			if self.useGUI == 1:
				value = self.app.fnameValue
			else:
				value = str(raw_input(parameter + " (Default: " + str(default) + "): "))
			
			# Set default value if there is no input
			if value == "":
				value = str(default)
				break
			elif parameter == "Image filename":
				# Check image filename is of correct filetype
				fpart = value.split('.',1)
				
				# Check file has an extension
				if len(fpart) > 1:
					ftype = fpart[-1]
				else:
					ftype = ""
				
				# Continue only if file extension is correct
				if ftype in IMAGE_TYPES:
					break
				else:
					if self.useGUI == 1:
						# Add correct extension if not correct
						value += ".jpg"
						break
					else:
						print(RED + "Image filename must have one of these extensions: " + str(IMAGE_TYPES) + CLEAR)
			else:
				# All video extensions supported, so no need to check
				break
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive start confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			if self.useGUI == 1:
				self.app.statlb.config(text="Status: " + confirm)
				Tk.update(self.root)
			else:
				print(YELLOW + confirm + CLEAR)
			
		try:
			# Receive finish confirmation message from the Pi.
			confirm = self.recv_msg(self.client_socket)
		except KeyboardInterrupt:
			# Send message to stop recording if Ctrl+C is pressed
			self.send_msg(self.client_socket, "Stop")
			confirm = self.recv_msg(self.client_socket)
		
		if confirm == None:
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			# Update GUI status
			if self.useGUI == 1:
				self.app.statlb.config(text="Status: " + confirm)
				Tk.update(self.root)
			else:
				print(GREEN + confirm + CLEAR)
		
		return value
	
	
	def filenameGUI(self, parameter):
		'''
		Get the filename if the GUI is used. In order to use the stop 
		button correctly, this has to be in a separate function 
		to processStrParameter.
		'''
		
		# Receive default, min, max parameters from Pi
		default = self.recv_msg(self.client_socket)

		# Input parameter value from terminal
		while True:
			if self.useGUI == 1:
				value = self.app.fnameValue
			else:
				value = str(raw_input(parameter + " (Default: " + str(default) + "): "))
			
			# Set default value if there is no input
			if value == "":
				value = str(default)
				break
			elif parameter == "Image filename":
				# Check image filename is of correct filetype
				fpart = value.split('.',1)
				
				# Check file has an extension
				if len(fpart) > 1:
					ftype = fpart[-1]
				else:
					ftype = ""
				
				# Continue only if file extension is correct
				if ftype in IMAGE_TYPES:
					break
				else:
					if self.useGUI == 1:
						value += ".jpg"
						break
					else:
						print(RED + "Image filename must have one of these extensions: " + str(IMAGE_TYPES) + CLEAR)
			else:
				# All video extensions supported, so no need to check
				break
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive start confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			if self.useGUI == 1:
				self.app.statlb.config(text="Status: " + confirm)
				Tk.update(self.root)
			else:
				print(YELLOW + confirm + CLEAR)
		
		return value
		
	
	def videoGUI(self):
		'''
		If the duration is infinite, then determine whether the stop 
		button of the GUI has been pressed.
		'''
		
		while True:
			# Stop the process by setting the value
			if self.procStop.value == 1:
				break
		# Send message to stop recording if Ctrl+C is pressed
		self.send_msg(self.client_socket, "Stop")
		self.confStop = self.recv_msg(self.client_socket)
		
	
	def printStats(self):
		'''
		Receive and print image/video stats after capture.
		'''
		
		# Receive properties of the image/video from the Raspberry Pi
		resolution = self.recv_msg(self.client_socket)
		framerate = self.recv_msg(self.client_socket)
		brightness = self.recv_msg(self.client_socket)
		contrast = self.recv_msg(self.client_socket)
		again = self.recv_msg(self.client_socket)
		dgain = self.recv_msg(self.client_socket)
		sharpness = self.recv_msg(self.client_socket)
		saturation = self.recv_msg(self.client_socket)
		xt = self.recv_msg(self.client_socket)
		
		if self.useGUI == 1:
			return resolution,framerate,brightness,contrast,sharpness,saturation,xt
		
		# Convert gain fractions into decimal
		if "/" in again:
			anum, aden = again.split('/')
			again = str(float(anum)/float(aden))
		
		if "/" in dgain:
			dnum, dden = dgain.split('/')
			dgain = str(float(dnum)/float(dden))
		
		# Convert contrast, sharpness, saturation to percentage
		contrast = str((int(contrast)+100)/2)
		sharpness = str((int(sharpness)+100)/2)
		saturation = str((int(saturation)+100)/2)
		
		if self.useGUI == 0:
			# Print the received properties
			print("\nProperties: ")
			print("    Resolution: " + resolution)
			print("    Framerate: " + framerate + " fps")
			print("    Brightness: " + brightness + " %")
			print("    Contrast: " + contrast + " %")
			print("    Analog gain: " + str(float(again)) + " dB")
			print("    Digital gain: " + str(float(dgain)) + " dB")
			print("    Sharpness: " + sharpness + " %")
			print("    Saturation: " + saturation + " %")
			print("    Exposure time: " + xt + " microseconds\n")
		
	
	def receiveFile(self, fname, typ):
		'''
		Receive an image or video from the Pi.
		'''
		
		if self.useGUI == 1:
			self.app.statlb.config(text="Status: Downloading file...")
			Tk.update(self.root)
		else:
			print(YELLOW + "Downloading file..." + CLEAR)
				
		# Must have Netcat installed on the command-line
		if typ == "Image":
			time.sleep(0.1)
			os.system("nc 192.168.1.1 60000 > ../../Images/" + fname)
		elif typ == "Trigger":
			while True:
				fnm = self.recv_msg(self.client_socket)
				print("Receiving...")
				if fnm == "Q":
					break
				else:
					time.sleep(0.1)
					os.system("nc 192.168.1.1 60000 > " + fnm)
		elif typ == "Video":
			time.sleep(0.1)
			os.system("nc 192.168.1.1 60000 > ../../Videos/" + fname)
		
		if self.useGUI == 1:
			# Update GUI status
			self.app.statlb.config(text="Status: Downloaded file")
			Tk.update(self.root)
		else:
			print(GREEN + "Downloaded file" + CLEAR)
		
	
	def sendTrigger(self):
		'''
		Send a trigger to immediately capture an image.
		'''
		
		while True:
			trigger = str(raw_input("Trigger (T for capture, Q for quit): ")).upper()
			self.send_msg(self.client_socket, trigger)
			
			# Capture trigger
			if trigger == "T":
				print("Capturing")
			
			# Quit trigger mode
			if trigger == "Q":
				break
		
	
	def sendCommand(self, useCmd):
		'''
		Send a command via terminal to the Raspberry Pi.
		'''
		
		# List of commands
		opt = ["B","C","F","G","H","I","N","O","P","Q","R","S","T","U","V","X"]
		self.durStop = 0
		
		if self.useGUI == 1:
			command = useCmd
		else:
			# Input command from terminal
			command = 0
			while command not in opt:
				command = str(raw_input("Input camera command: ")).upper()
				if command not in opt:
					print(RED + "Invalid command" + CLEAR)
				else:
					print(GREEN + "Command sent: " + command + CLEAR)
		
		# Send command
		self.send_msg(self.client_socket, command)
		
		# Send parameters and perform command
		# Set brightness
		if command == "B":
			self.processIntParameter("Brightness")
			
		# Set contrast
		elif command == "C":
			self.processIntParameter("Contrast")
			
		# Change framerate
		elif command == "F":
			self.processIntParameter("Framerate (fps)")
		
		# Set gain
		elif command == "G":
			print(CYAN + "Note: Gain of 0 automatically sets the gain" + CLEAR)
			self.processIntParameter("Gain")
			
		# Help
		elif command == "H":
			self.printCommands()
			
		# Caputre photo
		elif command == "I":
			filename = self.processStrParameter("Image filename")
			self.printStats()
			self.receiveFile(filename, "Image")
				
		# Network stream
		elif command == "N":
			print(CYAN + "Note: Press Ctrl+C to exit recording" + CLEAR)
			duration = self.processIntParameter("Duration (seconds)")
			if self.useGUI == 1 and self.durStop == "inf":
				self.procStop.value = 0
				prc = Process(target = self.networkStreamServer, args=(duration,))
				prc.start()
			else:
				self.networkStreamServer(duration)

		# Network subtract stream
		elif command == "O":
			print(CYAN + "Note: Press Ctrl+C to exit recording" + CLEAR)
			duration = self.processIntParameter("Duration (seconds)")
			if self.useGUI == 1 and self.durStop == "inf":
				self.procStop.value = 0
				prc = Process(target = self.networkStreamSubtract, args=(duration,))
				prc.start()
			else:
				self.networkStreamSubtract(duration)
		
		# Print camera settings
		elif command == "P":
			self.printStats()
			
		# Change resolution
		elif command == "R":
			self.processIntParameter("Width")
			if self.useGUI == 1:
				self.app.durValue = self.app.fnameValue
			self.processIntParameter("Height")
				
		# Set sharpness
		elif command == "S":
			self.processIntParameter("Sharpness")
		
		# Capture with trigger
		elif command == "T":
			print(CYAN + "Note: Option 1 uses the video port, which means there is a latency of 0-300 ms," + CLEAR)
			print(CYAN + "      but allows images to be taken in rapid succession." + CLEAR)
			print(CYAN + "      Option 2 uses the still port, which has a latency of 10-30 ms," + CLEAR)
			print(CYAN + "      but requires ~500 ms after capture to process and store the image." + CLEAR)
			while True:
				mode = str(raw_input("Enter mode (1 or 2): "))
				if mode == "1" or mode == "2":
					break
				else:
					print("Incorrect mode")
			self.send_msg(self.client_socket, mode)
			self.sendTrigger()
			self.receiveFile("", "Trigger")
			
		# Set saturation
		elif command == "U":
			self.processIntParameter("Saturation")
		
		# Capture stream
		elif command == "V":
			print(CYAN + "Note: Press Ctrl+C to exit recording" + CLEAR)
			self.processIntParameter("Duration (seconds)")
			if self.useGUI == 1 and self.durStop == "inf":
				self.fileStop = self.filenameGUI("Video filename")
				self.procStop.value = 0
				prc = Process(target = self.videoGUI)
				prc.start()
			else:
				filename = self.processStrParameter("Video filename")
				self.printStats()
				self.receiveFile(filename, "Video")
		
		# Change exposure time
		elif command == "X":
			print(CYAN + "Note: Exposure time of 0 automatically sets the exposure time" + CLEAR)
			self.processIntParameter("Exposure time (microseconds)")

		if self.useGUI == 1 and not command == "A" and not command == "N" and not command == "O" and not command == "V":
			self.app.dispProps()
		
		return command
	
	
	def runGUI(self):
		'''
		Initialise the camera GUI, and run the GUI loop.
		'''
		
		self.useGUI = 1
		self.root = Tk()
		self.root.geometry("640x480+150+150")
		self.app = cameraGUI(self.root, self)
		self.root.mainloop()
	
	
	def quitGUI(self, app):
		'''
		Quit the GUI, and tell the Raspberry Pi to quit also.
		'''
		
		app.quit()
		self.sendCommand("Q")
	
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		print(YELLOW + "Closing socket..." + CLEAR)
		self.client_socket.close()
