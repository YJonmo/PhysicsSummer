# CameraPython

This folder contains Python code to control the Raspberry Pi camera module.

## Files

- cameraLibServer.py: Library which contains functions for controlling the camera module of the Raspberry Pi, as well as functions which allow the Pi to be controlled from a remote computer.

- cameraLibClient.py: Library which contains functions to remotely control the Raspberry Pi from a remote computer.

- cameraServerTest.py: A server which runs indefinitely on the Raspberry Pi, which allows control of the camera module from a remote computer.

- cameraClientTest.py: A client which connects to the Raspberry Pi cameraServerTest.py script, and remotely controls the camera module.

- picamCommand.py: A script which runs indefinitely, and controls the camera module locally from the Raspberry Pi.

- picamTest.py: A set of test functions for the image mode of the camera module.

- pividTest.py: A set of test functions for the video mode of the camera module.

- launcher.sh: A bash script which allows the python camera module server to be launched on the Raspberry Pi at boot.

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

	g++ BackGroundSubb_Video.cpp -o BackGroundSubb_Video -I/usr/local/include/opencv2 -L/usr/local/lib -lopencv_core -lopencv_video -lopencv_highgui -lopencv_videoio -lopencv_imgcodecs -lopencv_imgproc


