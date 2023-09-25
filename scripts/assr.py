# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:55:24 2023

@author: elpid
"""

import pandas as pd
import pyxdf
import mne
import numpy as np

path_xdf ="C:/Users/elpid/Downloads/test data/sub-elpida/ses-pilot/eeg/sub-elpida_ses-pilot_task-assr_run-001_eeg.xdf"

data_xdf,header = pyxdf.load_xdf(path_xdf)

markers, eeg_sig = 2, 1 # elpida
eeg_scale = 1e6     # check the data I am getting

eeg_data = np.transpose(data_xdf[eeg_sig]['time_series'])/eeg_scale
eeg_ts = data_xdf[eeg_sig]['time_stamps']

assr_markers = data_xdf[markers]['time_series']
assr_ts = data_xdf[markers]['time_stamps']


# time stamps in seconds
zero_t = eeg_ts[0]
eeg_ts = eeg_ts-zero_t
assr_ts = assr_ts-zero_t

fs = 250
ch_names = ["O1","O2","P3","P4","P5","P6","T7","T8"] #correct the channels
ch_types = ["eeg"] * 8
n_channels = len(ch_names)
info = mne.create_info(ch_names = ch_names, sfreq = fs, ch_types='eeg')
raw = mne.io.RawArray(eeg_data, info, verbose=False)    # reads eeg as V

# set montage just to have different colors
montage = mne.channels.make_standard_montage('easycap-M1')
raw.set_montage(montage)    
  

# basic filtering
low_cut = 1
high_cut = 40       
filtered_data = raw.copy().filter(low_cut,high_cut,method='iir')
notch_freqs = [50]
filtered_data = filtered_data.notch_filter(freqs=notch_freqs, filter_length='auto', method='fir')

#shit
temp = filtered_data.get_data()
data = mne.io.RawArray(temp, info, verbose=False)



# plot
scaling = 100e-6
raw.plot(n_channels=n_channels, scalings=scaling, title='Raw Signals')

spect_raw = raw.compute_psd(method='welch',fmin=0,fmax=fs/2)
spect_raw.plot()

spect_filt = data.compute_psd(fmin=0,fmax=fs/2)
spect_filt.plot(xscale='log')
data.plot(n_channels=n_channels, scalings='auto' ,title='Filtered Signals')

data.info["bads"].extend(['O2','P4','T8'])   # elpida
#data.info["bads"].extend(['T8'])   # levi


final_data = mne.pick_types(data.info, eeg=True, exclude='bads')

#%% EVENTS

       
event_dict = {"rest":0, "assr":1}

onsets = np.array(assr_ts*fs, dtype=np.int32)  #onsets in frames
duration = np.ones_like(onsets)*30*fs #30 sec duration of stimuli
ids = np.array(assr_markers[:,0])  #start events 



events = np.c_[onsets,duration,ids]
#%%
epochs = mne.Epochs(data,events,event_id=event_dict,preload=True)
fig1 = epochs.plot(events=events)

epochs['rest'].compute_psd(fmin=0,fmax=fs/2).plot()
fig2 = epochs['rest'].average().plot()

epochs['assr'].compute_psd(fmin=0,fmax=fs/2).plot()

