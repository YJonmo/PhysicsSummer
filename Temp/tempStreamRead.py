'''
Modified code of DanielFlashReading.py.

Author: Damon Hutley
Date: 19th December 2016
'''


import h5py
import DAQT7_Objective as DAQ
import time
import datetime
import numpy as np
from multiprocessing import Process, Value, Array
import matplotlib.pyplot as plt


def SaveDataDAQ(TimeIndex, Voltages):						 
	'''
	This function save the recorded date in the HDF5 format. You don't need to call it when using for testing.
	'''
	
	File_name = "../../DAQT7/DAQT7" + str('%s' %datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S'))+ ".hdf5"
	file = h5py.File(File_name, "w")
	Spec_subgroup1 = file.create_group("DAQT7")
	file.create_dataset('DAQT7/Voltages', data = Voltages)
	file.create_dataset('DAQT7/TimeIndex', data = TimeIndex)
	Spec_subgroup1.attrs['DAQT7 Details'] = np.string_(DAQ1.getDetails())
	file.close()
	

def DAQ_Read_Process(DAQ_SamplingRate, ScansPerRead, Port):
	print("Starting")
	Read, DAQ_Starting[0], DAQ_Ending[0] = DAQ1.streamRead(DAQ_SamplingRate, ScansPerRead, Port)
 
	print len(Read[0])
	DAQ_Signal[0:len(Read[0])] = np.asarray(Read[0])
	

def DAQ_Read(No_DAC_Sample, Port):
	print("Starting")
	i = 0
	portIndex = 0
	portLength = len(Port)
	DAQ_Starting[0] = time.time()
	
	while i < No_DAC_Sample:
		DAQ_Signal[i], DAQ_Time[i] = DAQ1.readPort(Port[portIndex])
		portIndex = (portIndex + 1) % portLength
		
		if i % (No_DAC_Sample/100) == 0:
			print(str(i*100/(No_DAC_Sample)) + "%")
		
		i += 1
	
	DAQ_Ending[0] = time.time()


DAQ1 = DAQ.DetectDAQT7()

if DAQ1.Error == 1:
	print ('Cannot detect DAQ device')
else:
	while True:
		DurationOfReading = raw_input('Enter the duration of the reading in seconds (a number between 0.5 to 5 seconds): \n')
		try:
			DurationOfReading = float(DurationOfReading)
			if (float(DurationOfReading) < 0.5):
				print ('Duration time is too short. Enter a greater number')
			elif (float(DurationOfReading) > 10):
				print ('Duration is too long. Enter a smaller number')
			else:
				break
		except ValueError:
		   print("That's not a number!")  
		   print ('\n')

	if (DAQ1.Error == 0):
		StreamPort = ['AIN0', 'AIN1']		  
							 
		# This sampling rate in HZ is for when the internal buffer of DAQ is used
		# Check this link to see what sampling rates are appropriate:
		# https://labjack.com/support/datasheets/t7/appendix-a-1  
		DAQ_SamplingRate = 10000		
		ScansPerRead = int(DAQ_SamplingRate*DurationOfReading)
		
		# if you are using only on AIN then: No_DAC_Sample = DAQ_SamplingRate*2 
		# if you are using two AINs then: No_DAC_Sample = DAQ_SamplingRate*4
		No_DAC_Sample = ScansPerRead*len(StreamPort)
		
		DAQ_Signal = Array('d', np.zeros(shape=( No_DAC_Sample ,1), dtype = float ))
		DAQ_Time   = Array('d', np.zeros(shape=( No_DAC_Sample ,1), dtype = float ))
		DAQ_Starting = Array('d', np.zeros(shape=( 1 ,1), dtype = float ))
		DAQ_Ending = Array('d', np.zeros(shape=( 1 ,1), dtype = float ))	   

	################################## Start the the processes ###########################################
	if (DAQ1.Error == 0):
		while True:
			mode = input("Input mode (1 or 2): ")
			if mode == 1:
				DAQ_Read_Process(DAQ_SamplingRate, ScansPerRead, StreamPort)
				break
			elif mode == 2:
				DAQ_Read(No_DAC_Sample, StreamPort)
				break

	############################ Estimate the latencies of the devices ###################################   
	if (DAQ1.Error == 0):
		print(0, DAQ_Ending[0] - DAQ_Starting[0], No_DAC_Sample)
		DAQ_Time = np.linspace(0, DAQ_Ending[0] - DAQ_Starting[0], No_DAC_Sample)
		print(max(DAQ_Time))
		DAQ_Stack = []
		DAQ_Stack2 = []
		
		#if len(StreamPort) == 1:
			#DAQ_Time = [DAQ_Time]
			#DAQ_Signal = [DAQ_Signal]
		
		#elif len(StreamPort) == 2:
			#DAQ_Stack1 = DAQ_Signal[0::2]
			#DAQ_Stack2 = DAQ_Signal[1::2]
			#del(DAQ_Signal)
			#DAQ_Signal = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
			#DAQ_Signal[0] = DAQ_Stack1
			##for it in range(len(DAQ_Stack1)):
			##	DAQ_Stack2[it] -= DAQ_Stack1[it]
			#DAQ_Signal[1] = DAQ_Stack2
			
			#DAQ_Stack1 = DAQ_Time[0::2]
			#DAQ_Stack2 = DAQ_Time[1::2]
			#del(DAQ_Time)
			#DAQ_Time = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
			#DAQ_Time[0] = DAQ_Stack1
			#DAQ_Time[1] = DAQ_Stack2
			#print(max(DAQ_Signal[0]),max(DAQ_Signal[1]),max(DAQ_Time[0]),max(DAQ_Time[1]))
			##DAQ_Time = [DAQ_Time]
			##DAQ_Signal = [DAQ_Signal]
			
		#elif len(StreamPort) == 3:	 
			#DAQ_Stack1 = DAQ_Signal[0::2]
			#DAQ_Stack2 = DAQ_Signal[1::2]
			#DAQ_Stack3 = DAQ_Signal[2::2]
			#del(DAQ_Signal)
			#DAQ_Signal = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
			#DAQ_Signal[0] = DAQ_Stack1
			#DAQ_Signal[1] = DAQ_Stack2
			#DAQ_Signal[2] = DAQ_Stack3
			
			#DAQ_Stack1 = DAQ_Time[0::2]
			#DAQ_Stack2 = DAQ_Time[1::2]
			#DAQ_Stack3 = DAQ_Time[2::2]
			#del(DAQ_Time)
			#DAQ_Time = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
			#DAQ_Time[0] = DAQ_Stack1
			#DAQ_Time[1] = DAQ_Stack2
			#DAQ_Time[2] = DAQ_Stack3
			
		for i in range(len(StreamPort)):
			DAQ_Stack.append(np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float ))
			DAQ_Stack[i] = np.array(DAQ_Signal[i::len(StreamPort)])*-92.6+467.6-4.3
		
		del(DAQ_Signal)
		DAQ_Signal = DAQ_Stack
		
		for i in range(len(StreamPort)):
			DAQ_Stack2.append(np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float ))
			DAQ_Stack2[i] = DAQ_Time[i::len(StreamPort)]
		
		del(DAQ_Time)
		DAQ_Time = DAQ_Stack2
		
		SaveDataDAQ(DAQ_Time,DAQ_Signal) 
		
		for I in range(len(DAQ_Signal)):
			plt.plot(DAQ_Time[I], DAQ_Signal[I])
		
		DAQ1.close()
	
	##################################################################################################
	plt.show()
		
