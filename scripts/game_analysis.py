# Preliminary inspection of the game experiment
"""
Created on Wed Dec 13 16:11:04 2023

@author: elpid
"""


import numpy as np
import pyxdf
import mne
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#%% Extract data 
path = "C:/Users/elpid/Downloads/pilot_fatigue_test/elpida_131223/sub-elpida/ses-13_12_23/all/sub-elpida_ses-13_12_23_task-pilot_fatigue_test_acq-hugin_office_run-001_all.xdf"

data_xdf,header = pyxdf.load_xdf(path,dejitter_timestamps=False, synchronize_clocks=False)

for ind, stream in enumerate(data_xdf):
    if data_xdf[ind]['info']['name'] == ["HuginEEG"]:
        eeg_sig = ind
        
        eeg_scale = 1e6     # check the data I am getting
        eeg = np.transpose(stream['time_series'])/eeg_scale
        eeg_ts = stream['time_stamps']
        
    elif data_xdf[ind]['info']['name'] == ["LSL_Markers"]:
        markers_sig = ind
        
        markers = stream['time_series']
        markers_ts = stream['time_stamps']
        
    elif data_xdf[ind]['info']['name'] == ["HuginPPG"]: 
        ppg_sig = ind
        
        ppg = np.transpose(stream['time_series'])[0:3]
        ppg_ts = stream['time_stamps']


# time stamps in seconds
zero_t = eeg_ts[0]
eeg_ts = eeg_ts-zero_t
markers_ts = markers_ts-zero_t
ppg_ts = ppg_ts-zero_t


#%% Experimental events
BASELINELENGTH = 30
PVTSECTIONLENGTH = 60
MATHSECTIONLENGTH = 120
TETRISSECITONLEENGTH = 300
TETRISREPETITION = 3
SNAKESECITONLEENGTH = 300
SNAKEREPETITION = 3

#event ids
startBaseline = 1
startPvt = 2
pvtItemAppears = 3
startMaths = 4
correctAnswer = 5
startTetris = 6
tetrisFail = 7
levelGainTetris = 8
pauseTetris = 9
startSnake = 10
snakeFail = 11
snakeLvlUp = 12         # never happens !!!!
pauseSnake = 13


#%% EEG Setup 
layout = ["1", "2", "3", "4", "5", "6", "7", "8"]
ch_types = ["eeg"] * 8
sfreq = 250
info = mne.create_info(layout, sfreq, ch_types)
raw = mne.io.RawArray(eeg, info)

low_cut = 1
high_cut = 50      
filtered_data = raw.copy().filter(low_cut,high_cut,method='fir')
notch_freqs = [50]
filtered_data = filtered_data.notch_filter(freqs=notch_freqs, filter_length='auto', method='fir')


#%% PPG Setup
#none as of now

#%% PLOT DATA 
#EEG
filtered_data.plot(n_channels=len(layout), scalings='auto', title='Filtered Signals')

#%% make it as an animation                     !!!!!!!!!!!!!!!!!!!!!!!!
i = 15 #minute in the recording
samp2min = 60*25
interval_onset = i*samp2min
#PPG
fig, axs = plt.subplots(nrows=len(ppg), sharex=True)
fig.suptitle('PPG ')
for ch, ax in zip(range(len(ppg)), axs.ravel()):
    y = ppg[ch,interval_onset:interval_onset+samp2min]
    ax.plot(ppg_ts[interval_onset:interval_onset+samp2min],y)
    ax.set_ylabel('PPG data')
    ax.set_xlabel('Time [sec]')
plt.show()


#%% Baseline
for m, marker in enumerate(markers):
    if marker == startBaseline:
        t = markers_ts[m]
        dt = BASELINELENGTH*sfreq


#%% Tetris Game



#%% Snake Game


#%% PVT & Math

