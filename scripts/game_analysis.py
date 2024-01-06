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
filtered = filtered_data.get_data()[[0,1,2,3,4,5]]  # Should we remove the channels that are noisy ????

annotations = mne.Annotations(markers_ts,np.ones_like(markers_ts),markers[:,0])
filtered_data.set_annotations(annotations)
filtered_data.plot()


#%% PPG Setup
from matplotlib.animation import FuncAnimation


ppg_filtered = ppg_setup(ppg, fs_ppg, lowcut=0.8, highcut=11.9)

# Display PPG signals
plt.figure(figsize=(10, 6))
for channel in range(len(ppg_filtered)):
    plt.subplot(len(ppg_filtered), 1, channel+1)
    plt.plot(ppg_ts, ppg_filtered[channel], label=f'Channel {channel+1}')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
plt.tight_layout()
plt.show()


animation = True
channel = 0
if animation:
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], label='Channel 1')
    def update(frame):
        ax.clear()
        ax.plot(ppg_ts[:frame], ppg_filtered[channel, :frame], label='Channel 1')
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        ax.legend()
    ani = FuncAnimation(fig, update, frames=len(ppg_ts), interval=500, blit=False)
    plt.tight_layout()
    plt.show()

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
task_segments_ppg_dict = {}



# Extract segments for each task
for event_id, task_name in event_ids.items():
    task_segments, task_timestamps = extract_task_segments(event_id, filtered, eeg_ts, markers, markers_ts)
    task_segments_ppg, task_timestamps_ppg = extract_task_segments(event_id, ppg_filtered, ppg_ts, markers, markers_ts)

    
    if task_name in ['Tetris', 'Snake']:
        # Keep only 3 segments for Tetris and Snake tasks
        task_segments = task_segments[:, :get_task_duration(event_id)*3*fs_eeg]
        task_timestamps = task_timestamps[:get_task_duration(event_id)*3*fs_eeg]
        
        task_segments_ppg = task_segments_ppg[:, :get_task_duration(event_id)*3*fs_ppg]
        task_timestamps_ppg = task_timestamps[:get_task_duration(event_id)*3*fs_ppg]
        
    task_segments_dict[task_name] = (task_segments, task_timestamps)
    task_segments_ppg_dict[task_name] = (task_segments_ppg, task_timestamps_ppg)


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
import peak_detection_tools as peak
import feature_extraction_tools as feat


# Dictionaries to store processed task segments & features
task_segments_processed_dict = {}
task_rejected_epochs_dict = {}
n_epochs = {}

features_eeg_bands = {}
features_eeg_ratios = {}

features_ppg_fd={}
features_ppg_td={}
features_ppg_nl={}
        
        
        
for task in task_segments_dict.keys():
    if task == 'Baseline':
        # Baseline average
        baseline_average = baseline_av(task_segments_dict.get('Baseline')[0], task_segments_dict.get('Baseline')[1], threshold=100e-6, epoch_length=5, details=True)
    else:
        task_segments, task_timestamps = task_segments_dict.get(task, (None, None))
        task_segments_ppg, task_timestamps_ppg = task_segments_ppg_dict.get(task, (None, None))

    
        # Remove DC component
        task_segments = remove_dc(task_segments)
        
        # Epoch in 5sec epochs and remove epochs with peak-to-peak distance > 100uV
        epochs, epoch_timestamps, rejected_epochs =split_into_epochs_and_reject(task_segments, task_timestamps, threshold=100e-5, epoch_length=5, sample_rate=fs_eeg)
        epochs_ppg, epoch_timestamps_ppg, rejected_epochs_ppg =split_into_epochs_and_reject(task_segments_ppg, task_timestamps_ppg, threshold=100e6, epoch_length=30, sample_rate=fs_ppg)

        # Remove average baseline
        #epochs = [epoch - baseline_average for epoch in epochs]  # I think it adds noise 
        
        # Reshape and add to processed task dict
        n_epochs[task] = len(epochs)
        n_channels, n_times = epochs[0].shape
        
        reshaped_epochs = np.concatenate(epochs, axis=1)
        reshaped_epoch_timestamps = np.concatenate(epoch_timestamps, axis=0)
        rejected_epochs = np.array(rejected_epochs)
        
        task_segments_processed_dict[task] = (reshaped_epochs, reshaped_epoch_timestamps)
        task_rejected_epochs_dict[task] = (rejected_epochs)
        
        
        
        ################### EEG Features #####################
        # Frequency bands
        # does it make sense to split the alpha band ?????????   
        bands = {
            'theta': (4, 7),
            #'alpha1': (7, 10),
            #'alpha2': (10, 13),
            'alpha': (7,13),
            'beta': (14, 30)
            } 
        features_eeg_bands[task] = (frequency_features_eeg(epochs, fs_eeg, bands))
        #
        # Frequency ratios
        # (Using EEG spectral components to assess algorithms for detecting fatigue - Jap2009)
        ratios = {
            'alpha/beta': 1,
            'theta/beta': 2,
            '(theta+alpha)/beta': 3,
            '(theta+alpha)/(alpha+beta)': 4
            }
        features_eeg_ratios[task] = calculate_band_ratios(epochs, fs_eeg)
        
        
        ################### PPG Features #####################

        features_ppg_fd[task] = extract_ppg_features(epochs_ppg, fs_ppg, features='frequency domain')
        features_ppg_td[task] = extract_ppg_features(epochs_ppg, fs_ppg, features='time domain', td_win = 30)
        features_ppg_nl[task] = extract_ppg_features(epochs_ppg, fs_ppg, features='non-linear')


    
#%% Relative band powers and ratios on task and channel
# events ????????????

# from brokenaxes import brokenaxes
#bax = brokenaxes( xlims=((0, .1), (.4, .7)), hspace=.05)


for ch in [4]:
    for task in ['Pvt','Math','Tetris','Snake']:
        section = task
        
        fig, axs = plt.subplots(nrows=len(ratios), ncols=2, sharex=True)
        if ch>=3:
            fig.suptitle(f'{section} section in channel {ch+2}')
        else:
            fig.suptitle(f'{section} section in channel {ch+1}')

        for element, ax in zip({**bands, **ratios}, axs.ravel()):
            if element in bands:
                y = np.column_stack((features_eeg_bands[section][element]))
            elif element in ratios:
                y = np.column_stack((features_eeg_ratios[section][element]))

            ax.plot(y[ch])
            ax.set_ylabel(f'{element}')
            ax.set_xlabel('Epoch [5 sec]')     
        plt.show()
        
        
#%% Rejected epochs
fig, axs = plt.subplots(nrows=4, sharex=False)
fig.suptitle('Rejected epochs in each task: 1=rejected')
for task, ax in zip(['Pvt','Math','Tetris','Snake'], axs.ravel()):
    seg = len(task_rejected_epochs_dict[task])/3
    ax.plot(task_rejected_epochs_dict[task],'*:')
    ax.set_ylabel(f'{task}')
    plt.setp(ax, xticks=[0, seg, 2*seg])
plt.show()




#%%###########################################################################
##############################################################################
#Spectrogram of full recording
# Adjust ranges for each subject
from scipy import signal
import matplotlib.cm as cm


fig, axs = plt.subplots(nrows=len(filtered), sharex=True)
fig.suptitle('Spectrograms of good channels')
cmap = cm.get_cmap('inferno') 

for ch, ax in zip(range(len(filtered)), axs.ravel()):
    x = filtered[ch,:]
    
    f, t, Sxx = signal.spectrogram(x ,fs_eeg, nfft=512)
    mesh = ax.pcolormesh(t, f[0:60], Sxx[0:60,:], cmap=cmap, vmax=5e-12, vmin=0.5e-12) #,vmax=3.5e-12, vmin=0.5e-12
    ax.set_ylabel('Frequency [Hz]')
    ax.set_xlabel('Time [sec]')

fig.colorbar(mesh, ax= axs)
plt.xticks(ticks)

plt.show()


#%%
full_epochs, full_epoch_timestamps, full_rejected_epochs =split_into_epochs_and_reject(filtered, eeg_ts, threshold=100e-5, epoch_length=5, sample_rate=fs_eeg)
full_freq = frequency_features_eeg(full_epochs, fs_eeg, bands)
full_ratios = calculate_band_ratios(full_epochs, fs_eeg)

full_timestamps = np.concatenate(full_epoch_timestamps)

full_alpha = np.vstack(full_freq['alpha']).T
full_beta = np.vstack(full_freq['beta']).T
full_theta = np.vstack(full_freq['theta']).T


feats = {'theta': full_theta, 
     'alpha': full_alpha, 
     'beta': full_beta ,
     'alpha/beta': full_ratios['alpha/beta'].T,
     'theta/beta': full_ratios['theta/beta'].T,
     '(theta+alpha)/beta': full_ratios['(theta+alpha)/beta'].T,
     '(theta+alpha)/(alpha+beta)': full_ratios['(theta+alpha)/(alpha+beta)'].T}


fig, axs = plt.subplots(nrows=7, sharex=True)
fig.suptitle('EEG features through the recording (after drop of bad epochs)')
ch=3
for key, ax in zip(feats, axs.ravel()):   
    ax.plot(feats[key][ch] )
    ax.set_ylabel(f' {key} ')
    ax.set_xlabel('epochs [5 sec]')
    #ax.set_ylim([0,3])
#plt.xticks(ticks/5)
plt.show()

# Rejected epochs
fig, ax = plt.subplots(nrows=1, sharex=False)
fig.suptitle('Rejected epochs: 1=rejected')
ax.plot(full_rejected_epochs,'*:')
plt.show()

#%%
full_ppg, full_ppg_timestamps, full_rejected_ppg =split_into_epochs_and_reject(ppg_filtered, ppg_ts, threshold=100e6, epoch_length=30, sample_rate=fs_ppg)
full_fd = extract_ppg_features(full_ppg, fs_ppg, features='frequency domain')
full_td = extract_ppg_features(full_ppg, fs_ppg, features='time domain', td_win = 30)
full_nl = extract_ppg_features(full_ppg, fs_ppg, features='non-linear')

full_ppg_timestamps = np.concatenate(full_ppg_timestamps)


#%%
domain = full_fd
feature = 'LFHF'
y=[[],[],[]] 

for ch in range(3):
    for epoch in domain:
        y[ch].append(epoch[ch][feature])


fig, axs = plt.subplots(nrows=len(y), sharex=True)
fig.suptitle(f'{feature}')
for ch, ax in zip(y, axs.ravel()):
     ax.plot(ch)
     #ax.set_ylabel(f'channel {ch+1}')
     if feature == 'HR_mean':
         ax.set_ylim([60 ,120])
     elif feature == 'LFHF':
        ax.set_ylim([0,2])
plt.xticks(ticks/30)
plt.show()   
    


##############################################################################
##############################################################################
#%% HR_mean feature from PPG

hr_dict = {}

for ch in range(len(ppg)):
    tasks = ['Pvt','Math','Tetris','Snake']
    hr_task = {}
    for task, ax in zip(tasks, axs.ravel()):
        y = []
        for epoch in range(len(features_ppg_td[task])):
            y.append(features_ppg_td[task][epoch][ch]['HR_mean'])  
        hr_task[task] = y
    hr_dict[ch] = hr_task
    
  
for ch in range(len(hr_dict)):
    
    fig, axs = plt.subplots(nrows=len(tasks), ncols=1, sharex=False)
    fig.suptitle(f' channel {ch+1}')
    for task, ax in zip(tasks, axs.ravel()):
        hr = []
        for value in hr_dict[ch][task]:
            if isinstance(value, np.float64):
                if not np.isnan(value):
                    hr.append(value)
            else:
                print("The value is not of type numpy.float64")
        ax.plot(hr)
        ax.set_ylabel(f'{task}')
        ax.set_ylim([40, 120])
    plt.show()
    
#%% LFHF feature from PPG

lfhf_dict = {}

for ch in range(len(ppg)):
    tasks = ['Pvt','Math','Tetris','Snake']
    lfhf_task = {}
    for task, ax in zip(tasks, axs.ravel()):
        y = []
        for epoch in range(len(features_ppg_fd[task])):
            y.append(features_ppg_fd[task][epoch][ch]['LFHF'])  
        lfhf_task[task] = y
    lfhf_dict[ch] = lfhf_task
    
  
for ch in range(len(lfhf_dict)):
    
    fig, axs = plt.subplots(nrows=len(tasks), ncols=1, sharex=False)
    fig.suptitle(f' channel {ch+1}')
    for task, ax in zip(tasks, axs.ravel()):
        ax.plot(lfhf_dict[ch][task])
        ax.set_ylabel(f'{task}')
        ax.set_ylim([0, 2.5])
    plt.show()
 
#%% Baseline test
test_sig, test_ts = task_segments_dict.get('Baseline')
fig, axs = plt.subplots(nrows=len(test_sig), ncols=1, sharex=False)
fig.suptitle(f' Baseline')
for ch, ax in zip(test_sig, axs.ravel()):
    ax.plot(test_ts, ch)
    #ax.set_ylabel(f'channel {ch+1}')
    ax.set_ylim([-50e-6, 50e-6])
plt.show()

test_epoch_data, test_epoch_timestamps, test_rejected_epochs = split_into_epochs_and_reject(test_sig, test_ts, threshold=100e-6, epoch_length=5, sample_rate=250)
