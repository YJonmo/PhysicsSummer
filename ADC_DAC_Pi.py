'''
Adaptation of DAQT7_Objective.py for the Raspberry Pi.

Author: Damon Hutley
Date: 21st November 2016
'''


from ABE_ADCDACPi import ADCDACPi
import time
import numpy as np
import sys


class DetectPi:
	
	def __init__(self):
		'''
		Initialise ADC-DAC Pi.
		'''
		
		adcdac = ADCDACPi(1) # Create instance of ADCDACPi, with gain set to 1
		
		adcdac.set_adc_refvoltage(3.3) # Set reference voltage to 3.3 V
		
	
	def getDetails(self):
		'''
		Return details of ADC_DAC Pi.
		'''
	
	def writePort(self, Port, Volt):
		'''
		Write values to a DAC pin.
		'''
		
		adcdac.set_dac_voltage(Port, Volt) # Set DAC output voltage <Volt> on channel <Port>
	
	def readPort(self, Port):
		'''
		Read values from an ADC pin.
		'''
		
		adcdac.read_adc_voltage(Port, 0) # Read voltage from channel <Port> in single ended mode
	
	def streamRead(self, scanRate, scansPerRead, Port):
		'''
		Read analogue input values from an ADC pin, in stream mode.
		'''
	
	def close(self):
		'''
		Close ADC-DAC Pi.
		'''

