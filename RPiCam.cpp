/***********************************************************************
 * 
 * C++ library for the Raspberry Pi camera module. This library uses the 
 * raspicam C++ API found here: https://github.com/cedricve/raspicam.
 * 
 * Author: Damon Hutley
 * Date: 25th November 2016
 *
***********************************************************************/

/***********************************************************************
 * Header Files
***********************************************************************/

#include <ctime>
#include <fstream>
#include <iostream>
//#include <raspicam/raspicam_cv.h>
#include <raspicam/raspicam.h>
using namespace std;

/***********************************************************************
 * Objects
***********************************************************************/

/* Create the RaspiCam object. */
//raspicam::RaspiCam_Cv Camera;
raspicam::RaspiCam Camera;

/* Create the OpenCV object. */
//cv::Mat image;

/***********************************************************************
 * Functions
***********************************************************************/

/* Initialise the camera by setting the parameters, and opening the 
 * camera module. */
void initCamera() {
	//Camera.set(CV_CAP_PROP_FORMAT, CV_8UC1);
	cout << "Opening Camera..." << endl;
	if (!Camera.open()) {
		cerr << "Error opening the camera" << endl;
		//return -1;
	}
}

/* Capture a single image. */
void captureImage() {
	cout << "Capturing Image..." << endl;
	Camera.grab();
	//Camera.retrieve(image);
	Camera.release();
	cout << "Image Captured" << endl;
	//cv::imwrite("image.jpg",image);
	cout << "Image saved at image.jpg" << endl;
}

/* Capture a video. */
/*void captureVideo() {
	
}*/

/* Test of process command. */
void testFunction() {
	cout << "Success" << endl;
}

/* Process command from the terminal. */
char processCommand() {
	char command;
	cout << "Input camera command: ";
	cin >> command;
	
	return toupper(command);
}

/***********************************************************************
 * Main Code
***********************************************************************/

int main() {
	char command;
	
	initCamera();
	
	while (1) {
		command = processCommand();
		
		switch(command) {
			case 'I':
				captureImage();
				break;
				
			case 'T':
				testFunction();
				break;
			
			case 'Q':
				break;

			default:
				cout << "Command not recognised" << endl;
				break;
		}

		if (command == 'Q') {
			cout << "Quitting program..." << endl;
			break;
		}
	}
}
