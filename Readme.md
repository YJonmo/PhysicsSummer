# Physics Summer Work

Code for the Raspberry Pi. This includes an adaptation of the DAQT7_Objective library for Raspberry Pi, as well as a library for the camera module.

## Raspberry Pi Camera Installation

To install the raspicam library on the Raspberry Pi:

	cd raspicam-0.1.3
	mkdir build
	cd build
	cmake ..
	make
	sudo make install
	sudo ldconfig
	
To compile the program:
	
	g++ RPiCam.cpp -o RPiCam -I/usr/local/include -L/opt/vc/lib -lraspicam -lraspicam_cv -lmmal -lmmal_core -lmmal_util -lopencv_core -lopencv_highgui -lopencv_videoio -lopencv_imgcodecs -std=c++0x

To run the program:

	./RPiCam

## To-Do

-Implement video stream to vlc through network

-Implement remote control (could do through ssh)

-Lots and lots of testing
