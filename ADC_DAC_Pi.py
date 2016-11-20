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
	
	def getDetails(self):
		'''
		Return details of ADC_DAC Pi.
		'''
	
	def writePort(self, Port, Volt):
		'''
		Write values to a DAC pin.
		'''
	
	def readPort(self, Port):
		'''
		Read values from an ADC pin.
		'''
	
	def streamRead(self, scanRate, scansPerRead, Port):
		'''
		Read analogue input values from an ADC pin, in stream mode.
		'''
	
	def close(self):
		'''
		Close ADC-DAC Pi.
		'''

