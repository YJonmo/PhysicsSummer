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

time_start =  time.time()

# Functions to save data

No_iterations = 10
Time_Index = np.zeros(shape=(1, No_iterations ), dtype = float )

def SaveDataDAQ(TimeIndex, Voltages):                         
    '''
    This function save the recorded date in the HDF5 format. You don't need to call it when using for testing.
    '''
    
    File_name = "DAQT7" + str('%s' %datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S'))+ ".hdf5"
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
    
    #DAQ_Is_Read.value = 1


######################################################################################################
if __name__ == "__main__":
    
    DAQ1 = DAQ.DetectDAQT7()
    
    ######################################################################################################
    if DAQ1.Error == 1:
        print ('Cession failed: could not detect any devices')
    else:
        #PhotoDiod_Port = "AIN1"
        #DurationOfReading = 2    # Duration of reading in seconds.
        #Timer_Is_Over = Value('i', 0)
        #Timer_Is_Over.value = 0        
        
        #DAQ_Is_Read = Value('i', 0)
        #DAQ_Is_Read.value = 1
        
        
        while 1==1:
            DurationOfReading = raw_input('Enter the duration of the reading in seconds (a number between 0.5 to 5 seconds): \n')
            try:
                DurationOfReading = float(DurationOfReading)
                if (float(DurationOfReading) < 0.5):
                #if (float(Integration_Continious) < Spec_SamplingRate):
                    print ('Duration time is too short. Enter a greater number')
                elif (float(DurationOfReading) > 10):
                    print ('Duration is too long. Enter a smaller number')
                else:
                    break
            except ValueError:
               print("That's not a number!")  
               print ('\n')  
            
        ######################################################################################################
        if (DAQ1.Error == 0):
            #DAQ_Is_Read.value = 0
            StreamPort = ['AIN0']#['AIN0', 'AIN1']          
            DAQ_SamplingRate = 10000                     # this sampling rate in HZ is for when the internal buffer of DAQ is used
                                                         # check this link to see what sampling rates are appropriate:
                                                         # https://labjack.com/support/datasheets/t7/appendix-a-1          
            ScansPerRead = int(DAQ_SamplingRate*DurationOfReading)#/float(2))
            #No_DAC_Sample = DAQ_SamplingRate*4           # if you are using only on AIN then: No_DAC_Sample = DAQ_SamplingRate*2 
                                                         # if you are using two AINs then: No_DAC_Sample = DAQ_SamplingRate*4
            No_DAC_Sample = ScansPerRead*len(StreamPort)
            
            DAQ_Signal = Array('d', np.zeros(shape=( No_DAC_Sample ,1), dtype = float ))
            DAQ_Time   = Array('d', np.zeros(shape=( No_DAC_Sample ,1), dtype = float ))
            #DAQ_Index = Array('i', np.zeros(shape=( 1 ,1), dtype = int ))
            DAQ_Starting = Array('d', np.zeros(shape=( 1 ,1), dtype = float ))
            DAQ_Ending = Array('d', np.zeros(shape=( 1 ,1), dtype = float ))       
    
        ################################## Start the the processes ###########################################
        if (DAQ1.Error == 0):    
            #Pros_DAQ = Process(target=DAQ_Read_Process, args=(DAQ_SamplingRate, ScansPerRead, StreamPort))
            #Pros_DAQ.start()
            DAQ_Read_Process(DAQ_SamplingRate, ScansPerRead, StreamPort)

        ############################ Estimate the latencies of the devices ###################################   
        if (DAQ1.Error == 0):
            print(0, DAQ_Ending[0] - DAQ_Starting[0], No_DAC_Sample)
            #DAQ_Time = np.linspace(DAQ_Starting[0], (No_DAC_Sample*1)/float(DAQ_SamplingRate), No_DAC_Sample)
            DAQ_Time = np.linspace(0, DAQ_Ending[0] - DAQ_Starting[0], No_DAC_Sample)
            print(max(DAQ_Time))
            if len(StreamPort) == 2:
                DAQ_Stack1 = DAQ_Signal[0::2]
                DAQ_Stack2 = DAQ_Signal[1::2]
                del(DAQ_Signal)
                DAQ_Signal = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
                DAQ_Signal[0] = DAQ_Stack1
                DAQ_Signal[1] = DAQ_Stack2
                
                DAQ_Stack1 = DAQ_Time[0::2]
                DAQ_Stack2 = DAQ_Time[1::2]
                del(DAQ_Time)
                DAQ_Time = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
                DAQ_Time[0] = DAQ_Stack1
                DAQ_Time[1] = DAQ_Stack2
                print(max(DAQ_Signal[0]),max(DAQ_Signal[1]),max(DAQ_Time[0]),max(DAQ_Time[1]))
                #DAQ_Time = [DAQ_Time]
                #DAQ_Signal = [DAQ_Signal]
                
                
            elif len(StreamPort) == 3:     
                DAQ_Stack1 = DAQ_Signal[0::2]
                DAQ_Stack2 = DAQ_Signal[1::2]
                DAQ_Stack3 = DAQ_Signal[2::2]
                del(DAQ_Signal)
                DAQ_Signal = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
                DAQ_Signal[0] = DAQ_Stack1
                DAQ_Signal[1] = DAQ_Stack2
                DAQ_Signal[2] = DAQ_Stack3
                
                DAQ_Stack1 = DAQ_Time[0::2]
                DAQ_Stack2 = DAQ_Time[1::2]
                DAQ_Stack3 = DAQ_Time[2::2]
                del(DAQ_Time)
                DAQ_Time = np.zeros(shape=(len(StreamPort), No_DAC_Sample/len(StreamPort) ), dtype = float )
                DAQ_Time[0] = DAQ_Stack1
                DAQ_Time[1] = DAQ_Stack2
                DAQ_Time[2] = DAQ_Stack3
            
            elif len(StreamPort) == 1:
                DAQ_Time = [DAQ_Time]
                DAQ_Signal = [DAQ_Signal]
                    
            SaveDataDAQ(DAQ_Time,DAQ_Signal) 
            
            for I in range(len(DAQ_Signal)):
                plt.plot(DAQ_Time[I], DAQ_Signal[I])
            
            DAQ1.close()
        
        ##################################################################################################
        plt.show()
        
