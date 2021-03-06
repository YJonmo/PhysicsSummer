# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 16:39:11 2016

@author: Yaqub
"""

#import DAQT7_Objective as DAQ
import ADC_DAC_PiC
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py
import datetime

#%%
#DAQ1 = DAQ.DetectDAQT7()
DAQ1 = ADC_DAC_PiC.DetectPi()

SamplingRate = 10000  # 10kHz
DurationOfReading = 2
ScansPerRead = int(SamplingRate*DurationOfReading/float(2))
#Read, Starting, Ending = DAQ1.streamRead(SamplingRate, 'AIN1')
Read, Starting, Ending = DAQ1.streamRead(SamplingRate, ScansPerRead, 'AIN1')

plt.plot(Read[0])
plt.show()
