# ADC_DAC

This folder contains python code to run the ADC_DAC module on the Raspberry Pi.

## Files

- ADC_DAC_Pi.py: Library adaptation of the DAQT7_Objective library for the Raspberry Pi.

## Raspberry Pi Installation

The ADC_DAC code requires the ADCDACPi library. This can be installed by running the commands:

	cd Documents
	git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
	export PYTHONPATH=${PYTHONPATH}:~/Documents/ABElectronics_Python_Libraries/ADCDACPi/
