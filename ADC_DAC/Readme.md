# ADC_DAC

This folder contains python code to run the ADC_DAC module on the Raspberry Pi.

## Files

- ADC_DAC_Pi.py: Pure Python library adaptation of the DAQT7_Objective library for the Raspberry Pi. Achieves a sample rate of 12 kHz.

- ADC_DAC_PiC.py: C version of the library adaptation using a Python wrapper. Achieves a sample rate of 30 kHz.

- ADCTest.py: Test for the ADC_DAC_Pi library.

- ADCTestC.py: Test for the ADC_DAC_PiC library.

- ABE_ADCDACPi.c: C library to interface with the ADC_DAC module.

- ABE_ADCDACPi.h: Header file for the C library.

## Raspberry Pi Installation

The ADC_DAC code requires the ADCDACPi library. This can be installed by running the commands:

	cd Documents
	git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
	export PYTHONPATH=${PYTHONPATH}:~/Documents/ABElectronics_Python_Libraries/ADCDACPi/

The ADC_DAC_PiC code requires the ABE_ADCDACPi library .so file. This file can be obtained by compiling the library:

	gcc -shared -o libABE_ADCDACPi.so -fPIC ABE_ADCDACPi.c
