# CameraPython

This folder contains Python code to control the Raspberry Pi camera module.

## Files

- cameraLibServer.py: Library which contains functions for controlling the camera module of the Raspberry Pi, as well as functions which allow the Pi to be controlled from a remote computer.

- cameraLibClient.py: Library which contains functions to remotely control the Raspberry Pi from a remote computer.

- cameraServerTest.py: A server which runs indefinitely on the Raspberry Pi, which allows control of the camera module from a remote computer.

- cameraClientTest.py: A client which connects to the Raspberry Pi cameraServerTest.py script, and remotely controls the camera module.

- cameraClientGUI.py: Similar functionality to cameraClientTest.py, but runs with a GUI instead of command-line.

- picamCommand.py: A script which runs indefinitely, and controls the camera module locally from the Raspberry Pi.

- picamTest.py: A set of test functions for the image mode of the camera module.

- pividTest.py: A set of test functions for the video mode of the camera module.

- launcher.sh: A bash script which allows the python camera module server to be launched on the Raspberry Pi at boot.

- BackGroundSubbThread.cpp: C++ code for background subtraction with threading utilised in order to avoid frame drops. This code is used in cameraLibClient.py.

- BackGroundSubb_Video.cpp: Old C++ code with similar functionality to BackGroundSubbThread.cpp, but drops frames due to lack of threading.

- BackGroundSubb_Video_RPI.cpp: C++ code with identical functionality to BackGroundSubb_Video.cpp, but runs on the Raspberry Pi instead of a remote computer.

## Instructions - Running from remote computer

The CameraPython code can be run from a remote computer by connecting to the PiNet Wi-Fi network.
Once connected, open a terminal and enter the following commands:

	ssh pi@192.168.1.1
	cd Documents/PhysicsSummer/CameraPython
	python cameraServerTest.py
	
If prompted for a password, enter "PiPhysics".
If the python script is successfully runnning on the Raspberry Pi, open a new terminal, navigate to the git repository directory, and enter the following commands:

	cd CameraPython
	python cameraClientTest.py

If successful, a list of commands should appear.
The commands are:

	B: Set brightness
	C: Set contrast
	F: Set framerate
	G: Set gain
	H: Help
	I: Capture an image
	N: Stream to network
	O: Stream with image subtraction
	P: Get camera settings
	Q: Quit program
	R: Set resolution
	S: Set sharpness
	T: Capture with trigger
	U: Set saturation
	V: Capture a video
	X: Set exposure time

A prompt will appear to input a command.
Each command is a single letter and not case sensitive.
Input the command and press enter.

The I command takes a single image from the camera.
This command prompts for a filename to store the image in.
The filename must end in one of the following: ".jpg", ".jpeg", ".png", ".gif", ".bmp".
The default image filename is a timestamp, and used if no filename is entered into the prompt.
The image is downloaded from the Raspberry Pi to the remote computer, and stored in a folder named "Images".
The images folder must exist in the same directory that the git repository is contained in.

The T command is a trigger mode for taking images with small latency.
There are two trigger modes.
Mode 1 uses the video port.
This mode allows images to be taken in rapid succession.
However, it is possible that the image is taken before the trigger occurs.
This can be fixed by increasing the IMAGE_OFFSET parameter in the cameraLibServer.py code.
Additionally, the resolution cannot exceed 1920x1080 in this mode.
Mode 2 uses the image port.
This mode results in more consistent and higher quality images.
However, ~500 ms is required after the capture to process and store the image.
Additional images cannot be taken in this period of time.

The V command takes a video from the camera.
The program will ask for the duration of the video in seconds.
If no duration is entered, then the video will record indefinitely, until "Ctrl+C" is pressed in the terminal.
A filename will then be prompted.
A filename containing a timestamp is used if no filename is entered.
After the recording is completed, the video is downloaded to the remote computer, and stored in a folder named "Videos".
The videos folder must exist in the same directory that the git repository is contained in.

The N command streams a camera recording from the Raspberry Pi to the remote computer in real-time.
The program will ask for the duration of the video in seconds.
If no duration is entered, then the video will record indefinitely, until "Ctrl+C" is pressed in the terminal.
VLC will open and display the video stream.

The O command streams a camera recording from the Raspberry Pi to the remote computer in real-time, and performs image subtraction on the stream using OpenCV.
The program will ask for the duration of the video in seconds.
If no duration is entered, then the video will record indefinitely, until "Ctrl+C" is pressed in the terminal.
A window displaying the camera video will open, as well as another window displaying the image subtracted video.

The B, C, F, G, R, S, U, and X commands are setter functions.
For each command, the default, minimum, and maximum values are displayed for the corresponding property.
The default value is equal to the current value of the property.
If no value is entered, then the property is set to the default value.
Note that increasing the exposure time may lower the framerate, that increaing the framerate may lower the exposure time.

## Instructions - Running from remote computer with a GUI

The CameraPython code can be run with a GUI on a remote computer.
Mutliple terminals are still required to initialise the GUI.
Once connected to PiNet, open a terminal and enter the following commands:

	ssh pi@192.168.1.1
	cd Documents/PhysicsSummer/CameraPython
	python cameraServerTest.py
	
If prompted for a password, enter "PiPhysics".
If the python script is successfully runnning on the Raspberry Pi, open a new terminal, navigate to the git repository directory, and enter the following commands:

	cd CameraPython
	python cameraClientGUI.py

If successful, a window should appear containing a choice of camera modes, and an array of camera properties.

The Take Image command enters the Image mode.
In this mode, a filename may be entered.
If there is no filetype specified, then the filetype will default to ".jpg".
If the filename text box is left blank, then the filename will default to a string containing the current timestamp.
Pushing the start button will capture the image.
Once the image is captured, it will be downloaded into the Images folder, which must exist in the same directory as the git repository.

The Take Video command enters the Video mode.
In this mode, a filename may be entered.
If the filename text box is left blank, then the filename will default to a string containing the current timestamp.
A duration (in seconds) may also be entered.
If a duration is entered, then the video will record for that exact duration.
If the duration text box is left blank, then the video will record until the stop button is pressed.
Pressing the start button starts the video recording.
When the camera stops recording, the video is downloaded to the Images folder, which must exist in the same directory as the git repository.

The Stream to VLC command enters the Stream mode.
In this mode, a duration (in seconds) may be entered.
If a duration is entered, then the stream will last for that exact duration.
If the duration text box is left blank, then the stream will display until the stop button is pressed.
Pressing the start button opens VLC and starts the stream.
A stream delay of 1-5 seconds will exist due to the usage of VLC.

The Image Subtraction command enters the Subtract mode.
In this mode, a duration (in seconds) may be entered.
If a duration is entered, then the stream will last for that exact duration.
If the duration text box is left blank, then the stream will display until the stop button is pressed.
A background text box also exists.
If an image filename is entered into the background text box, then that image will be used as a static background which is subtracted from every video frame.
The image associated with the image filename must be contained within the Images folder, which must exist in the same directory as the git repository.
If no background is entered, then the each video frame will be subtracted by previous video frames.

The rest of the commands set camera properties.
The current, minimum, and maximum values for each property are displayed in the Properties frame.

## Instructions - Running from Raspberry Pi

The CameraPython code can be run directly from the Raspberry Pi.
On the Raspberry Pi, open a terminal, and run the command:

	cd Documents/PhysicsSummer/CameraPython
	python picamCommand.py

The code runs the same way as on a remote computer, but with a few differences:

- Images and Videos are stored on the Raspberry Pi as opposed to a remote computer

- The N command (network streaming) does not work

- The O command (image subtraction) runs on the Raspberry Pi as opposed to streaming on a remote computer. It runs a lot slower on the Raspberry Pi.

## Raspberry Pi Installation

The code requires the MP4Box package to place the raw video in a container, in order to playback at the correct framerate. This can be installed by:

	sudo apt-get install gpac

Netcat is also required to send image and video files to a remote computer. This can be installed by:

	sudo apt-get install netcat

Gstreamer is required to stream video to the remote computer, in order to perform image subtraction with openCV. This can be installed by:

	sudo apt-get install gstreamer-1.0

The Raspberry Pi uses an ad-hoc wireless network to connect to a remote computer. The ad-hoc wireless network can be created by first backing-up the current wireless settings:

	sudo cp /etc/network/interfaces /etc/network/interfaces-wifi

A new file is created to store the ad-hoc wireless settings:

	sudo nano /etc/network/interfaces-adhoc

Edit the file to contain the following code:

	auto lo
	iface lo inet loopback
	iface eth0 inet dhcp
	
	auto wlan0
	iface wlan0 inet static
	address 192.168.1.1
	netmask 255.255.255.0
	wireless-channel 11
	wireless-essid PiNet
	wireless-mode ad-hoc
	
Install a package to allow an IP address to be assigned to a remote computer:

	sudo apt-get install isc-dhcp-server

Edit the dhcpd config file:

	sudo nano /etc/dhcp/dhcpd.conf

Such that the file contains the following code:

	ddns-update-style interim;
	default-lease-time 600;
	max-lease-time 7200;
	authoritative;
	log-facility local7;
	subnet 192.168.1.0 netmask 255.255.255.0 {
	  range 192.168.1.5 192.168.1.150;
	}

To enable the ad-hoc wireless network, run the command:

	sudo cp /etc/network/interfaces-adhoc /etc/network/interfaces
	sudo reboot

To enable wifi, run the command:

	sudo cp /etc/network/interfaces-wifi /etc/network/interfaces
	sudo reboot

To run the python server script, type:

	python cameraServerTest.py

Alternatively, the python server script can be setup to run at boot. This can be setup by running the command:

	sudo crontab -e

The crontab file can then be edited to contain the following line:

	@reboot sh /home/pi/Documents/PhysicsSummer/CameraPython/launcher.sh

## Remote Computer Installation

Streaming video from the camera across the network requires vlc installed in the command-line on the remote computer. On macOS, run:

	brew install Caskroom/cask/vlc

Similarly, on Ubuntu/Mint, run:

	sudo apt-get install vlc

The remote computer can connect to the Raspberry Pi, assuming that the Raspberry Pi adhoc network is set-up correctly and enabled. 
The network "PiNet" should be listed in the wifi networks of the remote computer. 
Once the computer is connected to the Raspberry Pi, the computer can control the Raspberry Pi camera module by running the command:

	python cameraClientTest.py

Alternatively, the camera module can be controlled by remotely connecting to the Raspberry Pi terminal:

	ssh pi@192.168.1.1
	python picamCommand.py

However, remotely running the picamCommand script will not allow video streaming over the network, nor downloading image and video files directly to the remote computer.

## Image subtraction setup

The C++ code "BackGroundSubb_Video.cpp" is used to perform image subtraction on a network stream using OpenCV.
The network stream requires gstreamer, which must be installed before installing OpenCV.
Gstreamer can be installed by running the command:

	sudo apt-get install gstreamer-1.0
	sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav

OpenCV must be installed on the remote computer to run the C++ code.
To install OpenCV, go to http://opencv.org/downloads.html and download OpenCV 3.2.
Then, ensure that the following packages are installed:

	sudo apt-get install build-essential libgtk2.0-dev libjpeg-dev libtiff4-dev libjasper-dev libopenexr-dev cmake python-dev python-numpy python-tk libtbb-dev libeigen3-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev default-jdk ant libvtk5-qt4-dev

Enter the downloaded OpenCV directory, and perform the following commands:

	mkdir build
	cd build
	cmake ..
	make
	sudo make install
	sudo ldconfig

If changes are made to the C++ code, the code can be compiled with the following command:

	g++ -std=c++11 BackGroundSubb_Video.cpp -o BackGroundSubb_Video -I/usr/local/include/opencv2 -L/usr/local/lib -lopencv_core -lopencv_video -lopencv_highgui -lopencv_videoio -lopencv_imgcodecs -lopencv_imgproc


