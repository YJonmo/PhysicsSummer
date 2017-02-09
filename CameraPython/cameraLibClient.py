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
from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Style, Label, Entry


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
		Frame.__init__(self, parent)
		self.parent = parent
		self.camera = camera
		self.buttonWidth = 20
		self.initUI()
		
		self.commValue = 0
		self.fnameValue = 0
		self.durValue = 0
	
	def initUI(self):
		self.parent.title("Raspberry Pi Camera")
		self.style = Style()
		#self.style.configure("TButton", padding=(0,5,0,5), font='serif 10')
		self.style.theme_use("clam")
		
		pcolumn = 0
		ctcolumn = 1
		ccolumn = 2
		bcolumn = 0
		mintcolumn = 3
		mincolumn = 4
		maxtcolumn = 5
		maxcolumn = 6
		stcolumn = 7
		txtcolumn = 8
		
		#frame = Frame(self, relief=RAISED, borderwidth=1)
		#frame.pack(fill=BOTH, expand=1)
		
		self.pack(fill=BOTH, expand=1)
		
		#self.columnconfigure(1, weight=1)
		#self.columnconfigure(2, weight=1)
		self.columnconfigure(0, pad=7)
		#self.columnconfigure(1, pad=7)
		#self.rowconfigure(14, weight=1)
		#self.rowconfigure(5, pad=7)
		
		lbl = Label(self, text="Commands")
		lbl.grid(sticky=W, row=0, column=0, pady=4, padx=5)
		
		area = Text(self, width=66)
		area.grid(row=4, column=1, columnspan=4, rowspan=15, padx=5, sticky=E+W+S+N)
		
		imageButton = Button(self, text="Take Image", command= lambda: self.dispChange("I"), width=self.buttonWidth)
		imageButton.grid(row=1, column=bcolumn, pady=4)
		
		videoButton = Button(self, text="Take Video", command= lambda: self.dispChange("V"), width=self.buttonWidth)
		videoButton.grid(row=2, column=bcolumn, pady=4)
		
		networkButton = Button(self, text="Stream to VLC", command= lambda: self.dispChange("N"), width=self.buttonWidth)
		networkButton.grid(row=3, column=bcolumn, pady=4)
		
		isButton = Button(self, text="Image Subtraction", command= lambda: self.dispChange("O"), width=self.buttonWidth)
		isButton.grid(row=4, column=bcolumn, pady=4)
		
		resButton = Button(self, text="Set Resolution", command= lambda: self.dispChange("R"), width=self.buttonWidth)
		resButton.grid(row=5, column=bcolumn, pady=4)
		
		frButton = Button(self, text="Set Framerate", command= lambda: self.dispChange("F"), width=self.buttonWidth)
		frButton.grid(row=6, column=bcolumn, pady=4)
		
		xtButton = Button(self, text="Set Exposure Time", command= lambda: self.dispChange("X"), width=self.buttonWidth)
		xtButton.grid(row=7, column=bcolumn, pady=4)
		
		brButton = Button(self, text="Set Brightness", command= lambda: self.dispChange("B"), width=self.buttonWidth)
		brButton.grid(row=8, column=bcolumn, pady=4)
		
		coButton = Button(self, text="Set Contrast", command= lambda: self.dispChange("C"), width=self.buttonWidth)
		coButton.grid(row=9, column=bcolumn, pady=4)
		
		gnButton = Button(self, text="Set Gain", command= lambda: self.dispChange("G"), width=self.buttonWidth)
		gnButton.grid(row=10, column=bcolumn, pady=4)
		
		stButton = Button(self, text="Set Saturation", command= lambda: self.dispChange("U"), width=self.buttonWidth)
		stButton.grid(row=11, column=bcolumn, pady=4)
		
		shButton = Button(self, text="Set Sharpness", command= lambda: self.dispChange("S"), width=self.buttonWidth)
		shButton.grid(row=12, column=bcolumn, pady=4)
		
		quitButton = Button(self, text="Quit", command= lambda: self.camera.quitGUI(self), width=self.buttonWidth)
		quitButton.grid(row=13, column=bcolumn, pady=4)
		
		self.modelb = Label(self, text="Mode: Waiting")
		self.modelb.grid(sticky=W, row=1, column=1, columnspan=2, pady=4, padx=5)
		
		self.statlb = Label(self, text="Status: Connected to Raspberry Pi")
		self.statlb.grid(sticky=W, row=1, column=2, columnspan=2, pady=4, padx=5)
		
		self.but = Button(self)
		self.but2 = Button(self)
		self.lbl = Label(self)
		self.lbl2 = Label(self)
		self.txt = Entry(self)
		self.txt2 = Entry(self)
		
		#self.camera.sendCommand("A")
		#stats = self.camera.receiveAll()
		
		#reswlbl = Label(self, text="Width: ")
		#reswlbl.grid(sticky=W, row=4, column=pcolumn, pady=4, padx=5)
		
		#reshlbl = Label(self, text="Height: ")
		#reshlbl.grid(sticky=W, row=5, column=pcolumn, pady=4, padx=5)
		
		#frlbl = Label(self, text="Framerate: ")
		#frlbl.grid(sticky=W, row=6, column=pcolumn, pady=4, padx=5)
		
		#xtlbl = Label(self, text="Exposure Time: ")
		#xtlbl.grid(sticky=W, row=7, column=pcolumn, pady=4, padx=5)
		
		#brlbl = Label(self, text="Brightness: ")
		#brlbl.grid(sticky=W, row=8, column=pcolumn, pady=4, padx=5)
		
		#colbl = Label(self, text="Contrast: ")
		#colbl.grid(sticky=W, row=9, column=pcolumn, pady=4, padx=5)
		
		#gnlbl = Label(self, text="Gain: ")
		#gnlbl.grid(sticky=W, row=10, column=pcolumn, pady=4, padx=5)
		
		#stlbl = Label(self, text="Saturation: ")
		#stlbl.grid(sticky=W, row=11, column=pcolumn, pady=4, padx=5)
		
		#stlbl = Label(self, text="Sharpness: ")
		#stlbl.grid(sticky=W, row=12, column=pcolumn, pady=4, padx=5)
		
		#for i in range(27):
			#if i % 3 == 0:
				#currlab = Label(self, text="Current: ")
				#currlab.grid(sticky=W, row=(4+i/3), column=ctcolumn, pady=4, padx=5)
				
				#proplab = Label(self, text=str(stats[i]))
				#proplab.grid(sticky=W, row=(4+i/3), column=ccolumn, pady=4, padx=5)
			
			#if i % 3 == 1:
				#minlab = Label(self, text="Minimum: ")
				#minlab.grid(sticky=W, row=(4+i/3), column=mintcolumn, pady=4, padx=5)
				
				#minplab = Label(self, text=str(stats[i]))
				#minplab.grid(sticky=W, row=(4+i/3), column=mincolumn, pady=4, padx=5)
			
			#if i % 3 == 2:
				#maxlab = Label(self, text="Maximum: ")
				#maxlab.grid(sticky=W, row=(4+i/3), column=maxtcolumn, pady=4, padx=5)
				
				#maxplab = Label(self, text=str(stats[i]))
				#maxplab.grid(sticky=W, row=(4+i/3), column=maxcolumn, pady=4, padx=5)
		
		#for i in range(9):
			#setlab = Label(self, text="Set: ")
			#setlab.grid(sticky=W, row=(4+i), column=stcolumn, pady=4, padx=5)
			
			#txtlab = Text(self, height=1, width=10)
			#txtlab.grid(sticky=W, row=(4+i), column=txtcolumn, pady=4, padx=5)
	
	
	def dispChange(self, useCmd):
		self.but.grid_forget()
		self.but2.grid_forget()
		self.lbl.grid_forget()
		self.lbl2.grid_forget()
		self.txt.grid_forget()
		self.txt2.grid_forget()
		
		if useCmd == "I":
			self.modelb.config(text="Mode: Image")
			
			self.but = Button(self, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=2, column=3, pady=4, padx=5)
			
			self.lbl = Label(self, text="Enter Filename: ")
			self.lbl.grid(sticky=W, row=2, column=1, pady=4, padx=5)
			
			self.txt = Entry(self)
			self.txt.grid(sticky=W, row=2, column=2, pady=4, padx=5)
			
		elif useCmd == "V":
			self.modelb.config(text="Mode: Video")
			
			self.lbl = Label(self, text="Enter Filename: ")
			self.lbl.grid(sticky=W, row=2, column=1, pady=4, padx=5)
			
			self.txt = Entry(self)
			self.txt.grid(sticky=W, row=2, column=2, pady=4, padx=5)
			
			self.lbl2 = Label(self, text="Enter Duration: ")
			self.lbl2.grid(sticky=W, row=3, column=1, pady=4, padx=5)
			
			self.txt2 = Entry(self)
			self.txt2.grid(sticky=W, row=3, column=2, pady=4, padx=5)
			
			self.but = Button(self, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth/2)
			self.but.grid(sticky=W, row=3, column=3, pady=4, padx=5)
			
			self.but2 = Button(self, text="Stop", command=self.streamStop, width=self.buttonWidth/2)
			self.but2.grid(sticky=W, row=3, column=4, pady=4, padx=5)
			
		elif useCmd == "N":
			self.modelb.config(text="Mode: Stream")
			
			self.lbl2 = Label(self, text="Enter Duration: ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=4, padx=5)
			
			self.txt2 = Entry(self)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5)
			
			self.but = Button(self, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth/2)
			self.but.grid(sticky=W, row=2, column=3, pady=4, padx=5)
			
			self.but2 = Button(self, text="Stop", command=self.streamStop, width=self.buttonWidth/2)
			self.but2.grid(sticky=W, row=2, column=4, pady=4, padx=5)
			
		elif useCmd == "O":
			self.modelb.config(text="Mode: Subtract")
			
			self.lbl2 = Label(self, text="Enter Duration: ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=4, padx=5)
			
			self.txt2 = Entry(self)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5)
			
			self.but = Button(self, text="Start", command= lambda: self.retStr(useCmd), width=self.buttonWidth/2)
			self.but.grid(sticky=W, row=2, column=3, pady=4, padx=5)
			
			self.but2 = Button(self, text="Stop", command=self.streamStop, width=self.buttonWidth/2)
			self.but2.grid(sticky=W, row=2, column=4, pady=4, padx=5)
			
		elif useCmd == "R":
			self.modelb.config(text="Mode: Resolution")
		
			self.lbl2 = Label(self, text="Enter Width: ")
			self.lbl2.grid(sticky=W, row=2, column=1, pady=4, padx=5)
			
			self.txt2 = Entry(self)
			self.txt2.grid(sticky=W, row=2, column=2, pady=4, padx=5)
			
			self.lbl = Label(self, text="Enter Height: ")
			self.lbl.grid(sticky=W, row=3, column=1, pady=4, padx=5)
			
			self.txt = Entry(self)
			self.txt.grid(sticky=W, row=3, column=2, pady=4, padx=5)
			
			self.but = Button(self, text="Set", command= lambda: self.retStr(useCmd), width=self.buttonWidth)
			self.but.grid(sticky=W, row=3, column=3, pady=4, padx=5)
	
	def retStr(self, useCmd):
		self.fnameValue = self.txt.get()
		self.durValue = self.txt2.get()

		self.camera.sendCommand(useCmd)
	
	
	def streamStop(self):
		raise KeyboardInterrupt


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
		self.useGUI = 0
		
	
	def networkStreamServer(self, duration):
		'''
		Recieve a video stream from the Pi, and playback through VLC.
		'''
		
		# Determine the framerate of the stream
		frate = self.recv_msg(self.client_socket)
		
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
		except KeyboardInterrupt:
			self.send_msg(self.client_socket, "Stop")
			time.sleep(1)
		
		# Free connection resources
		print(GREEN + "Network stream closed" + CLEAR)
		connection.close()
		self.client_socket.close()
		player.terminate()
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
			gstcmd = "tcpclientsrc host=192.168.1.1 port=5000 ! gdpdepay ! rtph264depay ! video/x-h264, framerate=" + frate + "/1 ! avdec_h264 ! videoconvert ! appsink"
			subline = ['./BackGroundSubb_Video', '-vid', gstcmd]
			time.sleep(0.1)
			player = subprocess.Popen(subline)
			
			# Wait for executable to exit
			player.wait()
			
			# Free resources
			print(GREEN + "Network stream closed" + CLEAR)
			player.terminate()
		except:
			self.send_msg(self.client_socket, "Stop")
			time.sleep(1)
		
	
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
		result = []
		
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
		
		# Input parameter value from terminal
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
						print(RED + "Value is less than minimum" + CLEAR)
					elif float(value) > float(maximum):
						print(RED + "Value is greater than maximum" + CLEAR)
					elif value == "inf":
						value = str(sys.maxint)
						break
					else:
						break
				except ValueError:
					# Condition for parameter inputs that are not integers
					print(RED + "Not a number" + CLEAR)
		
		# Send parameter value to Pi
		self.send_msg(self.client_socket, value)
		
		# Receive confirmation message from the Pi.
		confirm = self.recv_msg(self.client_socket)
		if confirm == None:
			raise Exception("Command Failed (May need to lower resolution or framerate)")
		else:
			print(GREEN + confirm + CLEAR)
			
		return value
		
			
	def processStrParameter(self, parameter):
		'''
		Wait for parameter from the terminal, and then send string to the Pi.
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
			if self.useGUI == 1:
				self.app.statlb.config(text="Status: " + confirm)
				Tk.update(self.root)
			else:
				print(GREEN + confirm + CLEAR)
		
		return value
		
	
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
			
			if trigger == "T":
				print("Capturing")
			
			if trigger == "Q":
				break
		
	
	def sendCommand(self, useCmd):
		'''
		Send a command via terminal to the Raspberry Pi.
		'''
		
		# List of commands
		opt = ["B","C","F","G","H","I","N","O","P","Q","R","S","T","U","V","X"]
		
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
			self.networkStreamServer(duration)

		# Network subtract stream
		elif command == "O":
			print(CYAN + "Note: Press Ctrl+C to exit recording" + CLEAR)
			duration = self.processIntParameter("Duration (seconds)")
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
			filename = self.processStrParameter("Video filename")
			self.printStats()
			self.receiveFile(filename, "Video")
		
		# Change exposure time
		elif command == "X":
			print(CYAN + "Note: Exposure time of 0 automatically sets the exposure time" + CLEAR)
			self.processIntParameter("Exposure time (microseconds)")
		
		return command
	
	
	def runGUI(self):
		self.useGUI = 1
		self.root = Tk()
		self.root.geometry("640x480+300+300")
		#root.attributes('-zoomed', True)
		self.app = cameraGUI(self.root, self)
		self.root.mainloop()
	
	
	def quitGUI(self, app):
		app.quit()
		self.sendCommand("Q")
	
	
	def closeServer(self):
		'''
		Free server resources.
		'''
		
		# Close the connection and socket
		print(YELLOW + "Closing socket..." + CLEAR)
		self.client_socket.close()
