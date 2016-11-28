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
#include <string>
//#include <raspicam/raspicam_cv.h>
#include <raspicam/raspicam.h>
//#include <raspicam/raspicam_still_cv.h>
//#include <raspicam/raspicam_still.h>
using namespace std;

/***********************************************************************
 * Constants
***********************************************************************/

#define DEBUG 1
#define NOCV 1

/***********************************************************************
 * Objects
***********************************************************************/

/* Create the RaspiCam object. */
//raspicam::RaspiCam_Cv Camera;
raspicam::RaspiCam Camera;

/* Create the RaspiStill object. */
// raspicam::RapiCam_Still_Cv CameraStill;
//raspicam::RaspiCam_Still CameraStill;

/* Create the OpenCV object. */
//cv::Mat image;

/***********************************************************************
 * Functions
***********************************************************************/

/* Initialise the camera by setting the parameters, and opening the 
 * camera module. */
void initCamera() {
	if (DEBUG == 0) {
		//Camera.set(CV_CAP_PROP_FORMAT, CV_8UC1);
	}
	cout << "Opening Camera..." << endl;
	if (!Camera.open()) {
		cerr << "Error opening the camera" << endl;
	}
}

/* Capture a single image. */
void captureImage() {
	cout << "Capturing Image..." << endl;
	Camera.grab();
	if (NOCV == 0) {
		//Camera.retrieve(image);
	}
	Camera.release();
	cout << "Image Captured" << endl;
	if (NOCV == 0) {
		//cv::imwrite("image.jpg",image);
	}
	cout << "Image saved at image.jpg" << endl;
}

/* Capture a video. */
/*void captureVideo() {
	
}*/

/* Set the camera resoltion. */
void setResolution(int width, int height) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_FRAME_WIDTH, width);
		//Camera.set (CV_CAP_PROP_FRAME_HEIGHT, height);
	}
	cout << "Resolution changed" << endl;
}

/* Set the camera framerate. */
/*void setFramerate(int rate) {
	
}*/

/* Set the camera brightness. */
void setBrightness(int brightness) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_BRIGHTNESS, brightness);
	}
	cout << "Brightness changed" << endl;
}

/* Set the camera contrast. */
void setContrast(int contrast) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_CONTRAST, contrast);
	}
	cout << "Contrast changed" << endl;
}

/* Set the camera saturation. */
void setSaturation(int saturation) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_SATURATION, saturation);
	}
	cout << "Saturation changed" << endl;
}

/* Set the camera saturation. */
void setGain(int gain) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_GAIN, gain);
	}
	cout << "Gain changed" << endl;
}

/* Set the camera saturation. */
void setExposureTime(int speed) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_EXPOSURE, speed);
	}
	cout << "Exposure time changed" << endl;
}

/* Process camera parameters. */
int processParameters(string parString) {
	int parValue;
	
	cout << "Input ";
	cout << parString;
	cout << ": ";
	cin >> parValue;
	
	return parValue;
}

/* Print a list of commands. */
void printCommands() {
	cout << "\nList of commands:" << endl;
	cout << "	B: Set brightness" << endl;
	cout << "	C: Set contrast" << endl;
	cout << "	F: Set framerate (not implemented)" << endl;
	cout << "	G: Set gain" << endl;
	cout << "	H: Help" << endl;
	cout << "	I: Capture an image" << endl;
	cout << "	N: Stream to network (not implemented)" << endl;
	cout << "	Q: Quit program" << endl;
	cout << "	R: Set resolution" << endl;
	cout << "	S: Set saturation" << endl;
	cout << "	V: Capture a video (not implemented)" << endl;
	cout << "	X: Set exposure time\n" << endl;
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
	int brightness;
	int contrast;
	int saturation;
	int gain;
	int speed;
	int width;
	int height;
	
	initCamera();
	printCommands();
	
	while (1) {
		command = processCommand();
		
		switch(command) {
			case 'B':
				brightness = processParameters("Brightness");
				setBrightness(brightness);
				break;
				
			case 'C':
				contrast = processParameters("Contrast");
				setContrast(contrast);
				break;
			
			case 'F':
				cout << "Not yet implemented" << endl;
				break;
			
			case 'G':
				gain = processParameters("Gain");
				setGain(gain);
				break;
			
			case 'H':
				printCommands();
				break;
			
			case 'I':
				captureImage();
				break;
				
			case 'N':
				cout << "Not yet implemented" << endl;
				break;
				
			case 'Q':
				break;
				
			case 'R':
				width = processParameters("Width");
				height = processParameters("Height");
				setResolution(width, height);
				break;
			
			case 'S':
				saturation = processParameters("Saturation");
				setSaturation(saturation);
				break;
				
			case 'V':
				cout << "Not yet implemented" << endl;
				break;
			
			case 'X':
				speed = processParameters("Exposure Time");
				setExposureTime(speed);
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
