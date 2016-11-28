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
#include <raspicam/raspicam_still.h>
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
//raspicam::RapiCam_Still_Cv CameraStill;
raspicam::RaspiCam_Still CameraStill;

/***********************************************************************
 * Functions
***********************************************************************/

/* Initialise the camera by setting the parameters, and opening the 
 * camera module. */
void initCamera() {
	if (DEBUG == 0) {
		//Camera.set(CV_CAP_PROP_FORMAT, CV_8UC1);
	}
	cout << "Opening camera..." << endl;
	if (!Camera.open()) {
		cerr << "Error opening the camera" << endl;
	}
}

/* Capture a single image. */
void captureImage() {
	//cv::Mat image;
	string filename;
	
	cout << "Input filename: " << endl;
	cin.clear();
	cin.ignore(10000, '\n');
	cin >> filename;
	
	cout << "Capturing image..." << endl;
	//CameraStill.grab();
	if (NOCV == 0) {
		//CameraStill.retrieve(image);
	}
	CameraStill.release();
	cout << "Image captured" << endl;
	if (NOCV == 0) {
		//cv::imwrite(filename,image);
	}
	cout << "Image saved at ";
	cout << filename << endl;
}

/* Capture a video using openCV video writer. */
void captureVideo(int duration) {
	//cv::Mat image;
	//cv::VideoWriter writer;
	clock_t startTime;
	int codec;
	bool isColour;
	double fps;
	string filename;
	
	cout << "Input filename: " << endl;
	cin.clear();
	cin.ignore(10000, '\n');
	cin >> filename;
	
	if (NOCV == 0) {
		//codec = cv::CV_FOURCC('M', 'J', 'P', 'G');
		//isColour = (image.type() == CV_8UC3);
		//fps = 0;
		//writer.open(filename, codec, fps, image.size(), isColour);
	}
	
	startTime = clock();
	cout << "Recording started" << endl;
	
	while (((clock() - startTime)/CLOCKS_PER_SEC) < duration) {
		if (NOCV == 0) {
			Camera.grab();
			//Camera.retrieve(image);
			
			//writer.write(image);
		}
		else {
			continue;
		}
	}
	
	Camera.release();
	//writer.release();
	cout << "Recording finished" << endl;
	cout << "Video saved at ";
	cout << filename << endl;
}

/* Set the camera image resoltion. */
void setImageResolution(int width, int height) {
	if (DEBUG == 0) {
		//CameraStill.set (CV_CAP_PROP_FRAME_WIDTH, width);
		//CameraStill.set (CV_CAP_PROP_FRAME_HEIGHT, height);
	}
}

/* Set the camera video resoltion. */
void setVideoResolution(int width, int height) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_FRAME_WIDTH, width);
		//Camera.set (CV_CAP_PROP_FRAME_HEIGHT, height);
	}
}

/* Set the camera brightness. */
void setBrightness(int brightness) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_BRIGHTNESS, brightness);
		//CameraStill.set (CV_CAP_PROP_BRIGHTNESS, brightness);
	}
	cout << "Brightness changed" << endl;
}

/* Set the camera contrast. */
void setContrast(int contrast) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_CONTRAST, contrast);
		//CameraStill.set (CV_CAP_PROP_CONTRAST, contrast);
	}
	cout << "Contrast changed" << endl;
}

/* Set the camera saturation. */
void setSaturation(int saturation) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_SATURATION, saturation);
		//CameraStill.set (CV_CAP_PROP_SATURATION, saturation);
	}
	cout << "Saturation changed" << endl;
}

/* Set the camera saturation. */
void setGain(int gain) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_GAIN, gain);
		//CameraStill.set (CV_CAP_PROP_GAIN, gain);
	}
	cout << "Gain changed" << endl;
}

/* Set the camera saturation. */
void setExposureTime(int speed) {
	if (DEBUG == 0) {
		//Camera.set (CV_CAP_PROP_EXPOSURE, speed);
		//CameraStill.set (CV_CAP_PROP_EXPOSURE, speed);
	}
	cout << "Exposure time changed" << endl;
}

/* Process camera parameters. */
int processParameters(char parChar) {
	int parValue;
	int currValue;
	string parString;
	
	switch(parChar) {
		case 'W':
			parString = "width";
			currValue = -1;//Camera.get(CV_CAP_PROP_FRAME_WIDTH);
			break;
		
		case 'H':
			parString = "height";
			currValue = -1;//Camera.get(CV_CAP_PROP_FRAME_HEIGHT);
			break;
		
		case 'B':
			parString = "brightness";
			currValue = -1;//Camera.get(CV_CAP_PROP_FRAME_BRIGHTNESS);
			break;
		
		case 'C':
			parString = "contrast";
			currValue = -1;//Camera.get(CV_CAP_PROP_FRAME_CONTRAST);
			break;
		
		case 'S':
			parString = "saturation";
			currValue = -1;//Camera.get(CV_CAP_PROP_FRAME_SATURATION);
			break;
		
		case 'G':
			parString = "gain";
			currValue = -1;//Camera.get(CV_CAP_PROP_FRAME_GAIN);
			break;
		
		case 'X':
			parString = "exposure time";
			currValue = -1;//Camera.get(CV_CAP_PROP_FRAME_EXPOSURE);
			break;
			
		case 'D':
			parString = "duration";
			currValue = 0;
			break;
		
		default:
			currValue = -2;
	}

	cout << "Input ";
	cout << parString;
	cout << " (Current: ";
	cout << currValue;
	cout << "): ";

	cin.clear();
	cin.ignore(10000, '\n');
	cin >> parValue;
	
	return parValue;
}

/* Process command from the terminal. */
char processCommand() {
	char command;
	
	cout << "Input camera command: ";
	cin >> command;
	
	return toupper(command);
}

/* Print a list of commands. */
void printCommands() {
	cout << "\nList of commands:" << endl;
	cout << "	B: Set brightness" << endl;
	cout << "	C: Set contrast" << endl;
	cout << "	G: Set gain" << endl;
	cout << "	H: Help" << endl;
	cout << "	I: Capture an image" << endl;
	cout << "	N: Stream to network (not implemented)" << endl;
	cout << "	Q: Quit program" << endl;
	cout << "	S: Set saturation" << endl;
	cout << "	V: Capture a video" << endl;
	cout << "	X: Set exposure time\n" << endl;
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
	int duration;
	
	initCamera();
	printCommands();
	
	while (1) {
		command = processCommand();
		
		switch(command) {
			case 'B':
				brightness = processParameters('B');
				setBrightness(brightness);
				break;
				
			case 'C':
				contrast = processParameters('C');
				setContrast(contrast);
				break;
			
			case 'F':
				cout << "Not yet implemented" << endl;
				break;
			
			case 'G':
				gain = processParameters('G');
				setGain(gain);
				break;
			
			case 'H':
				printCommands();
				break;
			
			case 'I':
				width = processParameters('W');
				height = processParameters('H');
				setImageResolution(width, height);
				captureImage();
				break;
				
			case 'N':
				cout << "Not yet implemented" << endl;
				break;
				
			case 'Q':
				break;
			
			case 'S':
				saturation = processParameters('S');
				setSaturation(saturation);
				break;
				
			case 'V':
				width = processParameters('W');
				height = processParameters('H');
				setVideoResolution(width, height);
				duration = processParameters('D');
				captureVideo(duration);
				break;
			
			case 'X':
				speed = processParameters('X');
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

		cin.clear();
		cin.ignore(10000, '\n');
	}
}
