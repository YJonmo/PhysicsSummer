'''
Adaptation of the DAQT7_Objective library for the Raspberry Pi, using CTypes for speed gains.

Author: Damon Hutley
Date: 14th December 2016
'''


import ctypes
import time
import numpy as np
import sys


class DetectPi:
	
	def __init__(self):
		'''
		Initialise ADC-DAC Pi. The DAC gain factor is set to 1, which allows 
		the DAC output voltage to be set between 0 and 2.048 V. The DAC gain 
		factor may also be set to 2, which gives an output range of 0 to 3.3 V.
		'''
		
		# Import the adc_dac C library
		self.adclib = ctypes.CDLL('/home/pi/Documents/PhysicsSummer/ADC_DAC/libABE_ADCDACPi.so')
		
		# Initialise ADC and DAC SPI
		self.adclib.open_adc()
		self.adclib.open_dac()
		
		# Set reference voltage to 3.3 V and DAC gain to 2
		self.adclib.set_adc_refvoltage(ctypes.c_double(3.3))
		self.adclib.set_dac_gain(ctypes.c_int(2))
		
		return
		
	
	def getDetails(self):
		'''
		Return details of ADC_DAC Pi. This function does not currently return 
		any details, but this may change later.
		'''
		
		return
		
	
	def writePort(self, Port, Volt):
		'''
		Write values to a DAC pin. Values may be written to either channel 1 
		or channel 2. The maximum voltage is specified by the gain factor.
		Note: Setting a voltage of 5 V will return an error for exceeding 
		the maximum voltage.
		'''
		
		# Ensure port is of type list
		if type(Port) == str:
			Port = [Port]
		
		# Convert DAQT7 DAC ports to DAC Pi channels
		if "DAC0" in Port:
			channel = 1
		elif "DAC1" in Port:
			channel = 2
		
		if Volt > 3.3:
			print("Voltage exceeds maximum limit. Reducing to 3.3 V.")
			maxVolt = 3.3
		else:
			maxVolt = Volt
		
		# Set DAC output voltage <Volt> on channel <channel>
		self.adclib.set_dac_voltage(ctypes.c_double(maxVolt), ctypes.c_int(channel))
		
		return
		
	
	def readPort(self, Port):
		'''
		Read values from an ADC pin. Values may be read from either channel 1 
		or channel 2. 
		'''
		
		# Ensure port is of type list
		if type(Port) == str:
			Port = [Port]
		
		# Convert DAQT7 AIN ports to ADC Pi channels
		if "AIN0" in Port:
			channel = 1
		elif "AIN1" in Port:
			channel = 2
		
		# Read voltage from channel <channel> in single ended mode
		voltRead = self.adclib.read_adc_voltage(ctypes.c_int(channel), ctypes.c_int(0))
		print(voltRead)
		
		return np.float(voltRead), time.time()
		
	
	def streamRead(self, scanRate, scansPerRead, Port):
		'''
		Read analogue input values from an ADC pin, in stream mode.
		'''
		
		# Ensure port is of type list
		if type(Port) == str:
			Port = [Port]
		
		# Convert DAQ ports to ADC channels
		channel = []
		for p in Port:
			if p == "AIN0":
				channel.append(1)
			elif p == "AIN1":
				channel.append(2)
			else:
				channel.append(1)
		
		# Initialise array and time values
		Read = [0]
		StartingMoment = 0
		FinishingMoment = 0
		scansPerRead = int(scansPerRead)
		
		# Determine timing characteristics
		duration = scansPerRead/float(scanRate)
		dt = 1/float(scanRate)
		
		# Allow for alternation between multiple ports
		portIndex = 0
		portLength = len(channel)
		
		# Loop for the duration
		StartingMoment = time.time()
		while (time.time()-StartingMoment) < duration:
			# Read the ADC value and append to an array
			voltRead = self.adclib.read_adc_voltage(ctypes.c_int(channel[portIndex]), ctypes.c_int(0))
			Read.append(voltRead)
			portIndex = (portIndex + 1) % portLength
			
			# Wait for the program to run at the correct frequency
			#lastReadTime = readTime
			#readTime = time.time()
			#if readTime - lastReadTime < dt:
				#time.sleep(dt - readTime + lastReadTime)
			
		# Calculate and print elapsed time
		FinishingMoment = time.time()
		print ('Elapsed time %f seconds' % (FinishingMoment - StartingMoment))
		print(np.mean(Read))
		
		return Read, StartingMoment, FinishingMoment
		
	
	def close(self):
		'''
		Close ADC-DAC Pi.
		'''
		
		self.adclib.close_adc()
		self.adclib.close_dac()


		

