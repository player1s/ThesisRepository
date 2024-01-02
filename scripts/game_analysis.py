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
from helper_functions import *


#%% Extract data from csv file
path = "C:/Users/elpid/Downloads/fatigue_test/Leonard/sub-leonard/ses-20_12_23/all/sub-leonard_ses-20_12_23_task-fatigue_test_acq-hugin_shielded_run-001_all.xdf"

data_xdf,header = pyxdf.load_xdf(path,dejitter_timestamps=False, synchronize_clocks=False)

for ind, stream in enumerate(data_xdf):
    if data_xdf[ind]['info']['name'] == ["HuginEEG"]:
        eeg_sig = ind
        
        eeg_scale = 1e6     # signals in uV, mne input in V
        eeg = np.transpose(stream['time_series'])/eeg_scale
        eeg_ts = stream['time_stamps']
        fs_eeg = int(stream['info']['effective_srate'])
        #fs_eeg=250
        
    elif data_xdf[ind]['info']['name'] == ["LSL_Markers"]:
        markers_sig = ind
        
        markers = stream['time_series']
        markers_ts = stream['time_stamps']
        
    elif data_xdf[ind]['info']['name'] == ["HuginPPG"]: 
        ppg_sig = ind
        
        ppg = np.transpose(stream['time_series'])[0:3]
        ppg_ts = stream['time_stamps']
        fs_ppg =  int(stream['info']['effective_srate'])


# time stamps in seconds
zero_t = eeg_ts[0]
eeg_ts = eeg_ts-zero_t
markers_ts = markers_ts-zero_t
ppg_ts = ppg_ts-zero_t


#%% Experimental events
BASELINELENGTH = 30
PVTSECTIONLENGTH = 150
MATHSECTIONLENGTH = 150
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
inCorrectAnswer = 6
startTetris = 7
tetrisFail = 8
levelGainTetris = 9
pauseTetris = 10
startSnake = 11
snakeFail = 12
snakeLvlUp = 13
pauseSnake = 14

ticks = []
tick_labels = []

for m, marker in enumerate(markers):
    if marker== startBaseline or marker==startPvt or marker ==startMaths or marker==startSnake or marker==startTetris:
        ticks.append(markers_ts[m])
        tick_labels.append(markers[m])

# ticks at the start of each exp. phase
ticks = np.asarray(ticks)
tick_labels = np.asarray(tick_labels) 

#%% EEG Setup 

filtered_data, info = eeg_setup(eeg, fs_eeg)
filtered = filtered_data.get_data()


#%% Extract the task segments
event_ids = {
    1: "Baseline",
    2: "Pvt",
    4: "Math",
    7: "Tetris",
    11: "Snake",
}

# Dictionary to store task segments
task_segments_dict = {}

# Extract segments for each task
for event_id, task_name in event_ids.items():
    task_segments, task_timestamps = extract_task_segments(event_id, filtered, eeg_ts, markers, markers_ts)
    
    if task_name in ['Tetris', 'Snake']:
        # Keep only 3 segments for Tetris and Snake tasks
        task_segments = task_segments[:, :get_task_duration(event_id)*3*fs_eeg]
        task_timestamps = task_timestamps[:get_task_duration(event_id)*3*fs_eeg]
        
    task_segments_dict[task_name] = (task_segments, task_timestamps)


test = False
if test:
    # Access segments for a specific task along with timestamps
    tetris_task_segments, tetris_task_timestamps = task_segments_dict.get("Tetris", (None, None))
    
    fig, axs = plt.subplots(nrows=len(tetris_task_segments), sharex=True)
    fig.suptitle('Tetris')
    for ch, ax in zip(range(len(tetris_task_segments)), axs.ravel()):
        ax.plot(tetris_task_timestamps, tetris_task_segments[ch])
        ax.set_ylabel(f'channel {ch}')
        ax.set_xlabel('Time [sec]')    
    plt.show()
    
    snake_task_segments, snake_task_timestamps = task_segments_dict.get("Snake", (None, None))
    
    fig, axs = plt.subplots(nrows=len(snake_task_segments), sharex=True)
    fig.suptitle('Snake')
    for ch, ax in zip(range(len(snake_task_segments)), axs.ravel()):
        ax.plot(snake_task_timestamps, snake_task_segments[ch])
        ax.set_ylabel(f'channel {ch}')
        ax.set_xlabel('Time [sec]')    
    plt.show()



#%% Process each segment
from helper_functions import*
from scipy.signal import welch


# Baseline average
baseline_average = baseline_av(task_segments_dict.get('Baseline')[0], task_segments_dict.get('Baseline')[1], details=True)

# Dictionary to store processed task segments
task_segments_processed_dict = {}
task_rejected_epochs_dict = {}

for task in task_segments_dict.keys():
    task_segments, task_timestamps = task_segments_dict.get(task, (None, None))

    # Remove DC component
    task_segments = remove_dc(task_segments)
    
    # Epoch in 5sec epochs and remove epochs with peak-to-peak distance > 100uV
    epochs, epoch_timestamps, rejected_epochs =split_into_epochs_and_reject(task_segments, task_timestamps, threshold=100e-6, epoch_length=5)
    
    # Remove average baseline
    #epochs = [epoch - baseline_average for epoch in epochs]  # I think it adds noise 
    
    # Reshape and add to processed task dict
    n_epochs = len(epochs)
    n_channels, n_times = epochs[0].shape
    
    reshaped_epochs = np.concatenate(epochs, axis=1)
    reshaped_epoch_timestamps = np.concatenate(epoch_timestamps, axis=0)
    rejected_epochs = np.array(rejected_epochs)
    
    task_segments_processed_dict[task] = (reshaped_epochs, reshaped_epoch_timestamps)
    task_rejected_epochs_dict[task] = (rejected_epochs)
    
    
    # Features
    bands = {
        'theta': (4, 7),
        'alpha1': (7, 10),
        'alpha2': (10, 13),
        'beta': (14, 30)
    }

    band_powers = {band: [] for band in bands}

for epoch in epochs:
    freqs, psd = welch(epoch, fs_eeg)

    for band, (fmin, fmax) in bands.items():
        idx_band = np.where((freqs >= fmin) & (freqs <= fmax))[0]  # Get indices as 1D array
        if len(idx_band) > 0:  # Check if idx_band is not empty
            band_psd = psd[:,idx_band]
            epoch_band_power = np.trapz(band_psd, freqs[idx_band])
            total_power = np.trapz(psd, freqs)
            band_powers[band].append(epoch_band_power / total_power)
            
        # Calculate total power
        total_power = np.trapz(psd, freqs)

        # Calculate relative power for each band
        for band in bands:
            band_powers[band].append(epoch_band_powers[band] / total_power)


#%%
# from brokenaxes import brokenaxes


# fig, axs = plt.subplots(nrows=5, sharex=False)
# fig.suptitle('Baseline section')
# #bax = brokenaxes( xlims=((0, .1), (.4, .7)), hspace=.05)

# for task, ax in zip(task_segments_dict.keys(), axs.ravel()):
#     ax.plot(task_segments_dict[task][1],'r')
#     ax.set_ylabel(f'{task}')
#     ax.set_xlabel('Time [sec]')  
    
# plt.show()


