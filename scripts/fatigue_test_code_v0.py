# fatigue test1 :
# ________________
# pvt + arithmetics - PPG
# tetronimo         - EEG
# pvt + arithmetics - PPG

"""
Created on Fri Dec  1 12:45:33 2023

@author: elpid
"""
import numpy as np
import pyxdf
import mne
import matplotlib.pyplot as plt



eeg_path = "C:/Users/elpid/Downloads/test data/sub-elpida/ses-05_12_23/eeg/sub-elpida_ses-05_12_23_task-fatigue_test2_acq-hugin_run-001_eeg.xdf"
ppg1_path = "C:/Users/elpid/Downloads/test data/sub-elpida/ses-05_12_23/ppg1/sub-elpida_ses-05_12_23_task-fatigue_test2_acq-hugin_run-001_ppg1.xdf"
ppg2_path = "C:/Users/elpid/Downloads/test data/sub-elpida/ses-05_12_23/ppg2/sub-elpida_ses-05_12_23_task-fatigue_test2_acq-hugin_run-001_ppg2.xdf"

eeg_xdf,header = pyxdf.load_xdf(eeg_path,dejitter_timestamps=False, synchronize_clocks=False)
ppg1_xdf,header = pyxdf.load_xdf(ppg1_path,dejitter_timestamps=False, synchronize_clocks=False)
ppg2_xdf,header = pyxdf.load_xdf(ppg2_path,dejitter_timestamps=False, synchronize_clocks=False)


eeg_scale = 1e6     # check the data I am getting
eeg_data = np.transpose(eeg_xdf[0]['time_series'])/eeg_scale
ppg1_data = np.transpose(ppg1_xdf[0]['time_series'])[0:3]
ppg1_time = np.array(ppg1_xdf[0]['time_stamps']-ppg1_xdf[0]['time_stamps'][0])
ppg2_data = np.transpose(ppg2_xdf[0]['time_series'])[0:3]
ppg2_time = np.array(ppg2_xdf[0]['time_stamps']-ppg2_xdf[0]['time_stamps'][0])



layout = ["1", "2", "3", "4", "5", "6", "7", "8"]
ch_types = ["eeg"] * 8
sfreq = 250
info = mne.create_info(layout, sfreq, ch_types)
raw = mne.io.RawArray(eeg_data, info)

low_cut = 1
high_cut = 50      
filtered_data = raw.copy().filter(low_cut,high_cut,method='fir')
notch_freqs = [50]
filtered_data = filtered_data.notch_filter(freqs=notch_freqs, filter_length='auto', method='fir')

#%% EXPERIMENT EVENTS
t_tetris = 0*60
dt_tetris = 17*60
t_eval1 = t_tetris + dt_tetris
dt_eval1 = 5*60
t_snake = t_eval1 + dt_eval1 + 2*60
dt_snake = 13*60
t_eval2 = t_snake + dt_snake
dt_eval2 = 5*60
ticks = np.asarray([t_tetris, t_eval1, t_snake, t_eval2])

#%% PLOT DATA 
#EEG
filtered_data.plot(n_channels=len(layout), scalings='auto', title='Filtered Signals')

#PPG1
fig, axs = plt.subplots(nrows=len(ppg1_data), sharex=True)
fig.suptitle('PPG before')
for ch, ax in zip(range(len(ppg1_data)), axs.ravel()):
    y = ppg1_data[ch,:]
    ax.plot(ppg1_time,y)
    ax.set_ylabel('PPG data')
    ax.set_xlabel('Time [sec]')
plt.show()

#PPG2
fig, axs = plt.subplots(nrows=len(ppg2_data), sharex=True)
fig.suptitle('PPG after')
for ch, ax in zip(range(len(ppg2_data)), axs.ravel()):
    y = ppg2_data[ch,:]
    ax.plot(ppg2_time,y)
    ax.set_ylabel('PPG data')
    ax.set_xlabel('Time [sec]')
plt.show()


#%%
plots = True
if plots:
    import matplotlib.pyplot as plt
    
    
    theta_min, theta_max = 4, 7
    alpha1_min, alpha1_max = 8, 10
    alpha2_min, alpha2_max = 10, 13
    beta_min, beta_max = 14, 30
    
    focus_seg = 5 *sfreq  
    
    def bandpower(data, sf, band, window_sec=None, relative=False):
        """Compute the average power of the signal x in a specific frequency band.
    
        Parameters
        ----------
        data : 1d-array
            Input signal in the time-domain.
        sf : float
            Sampling frequency of the data.
        band : list
            Lower and upper frequencies of the band of interest.
        window_sec : float
            Length of each window in seconds.
            If None, window_sec = (1 / min(band)) * 2
        relative : boolean
            If True, return the relative power (= divided by the total power of the signal).
            If False (default), return the absolute power.
    
        Return
        ------
        bp : float
            Absolute or relative band power.
        """
        from scipy.signal import welch
        from scipy.integrate import simps
        band = np.asarray(band)
        low, high = band
    
        # Define window length
        if window_sec is not None:
            nperseg = window_sec * sf
        else:
            nperseg = (2 / low) * sf
    
        # Compute the modified periodogram (Welch)
        freqs, psd = welch(data, sf, nperseg=nperseg)
    
        # Frequency resolution
        freq_res = freqs[1] - freqs[0]
    
        # Find closest indices of band in frequency vector
        idx_band = np.logical_and(freqs >= low, freqs <= high)
    
        # Integral approximation of the spectrum using Simpson's rule.
        bp = simps(psd[idx_band], dx=freq_res)
    
        if relative:
            bp /= simps(psd, dx=freq_res)
        return bp
    
    theta = []
    alpha1 = []
    alpha2 = []
    beta = []
    ch = 1
    filt = filtered_data.get_data()[ch] # 1,2,4,5,6
     
    for i in range(0,int(len(filt)/(focus_seg))):
        data_temp = filt[i*focus_seg:i*focus_seg+focus_seg]
        bp_a1 = bandpower(data_temp, sfreq, band=[alpha1_min,alpha1_max], window_sec=5)
        bp_a2 = bandpower(data_temp, sfreq, band=[alpha2_min,alpha2_max], window_sec=5)
        bp_b = bandpower(data_temp, sfreq, band=[beta_min,beta_max], window_sec=5)
        bp_th = bandpower(data_temp, sfreq, band=[theta_min,theta_max], window_sec=5)
    
        alpha1.append(bp_a1)
        alpha2.append(bp_a2)
        beta.append(bp_b)
        theta.append(bp_th)
    
        
    
    fig,ax = plt.subplots()
    x=np.arange(0,len(alpha1),1)
    ax.plot(x, alpha1, label='alpha1')
    ax.plot(x, alpha2, label='alpha2',color='purple')
    ax.plot(x, beta, label='beta')
    ax.plot(x, theta, label='theta')
#    ax.set_ylim([0,2.5e-11])
    ax.set_title(f'Average of {focus_seg/sfreq} secs in channel {ch+1}')
    ax.set_xlabel(f'x{focus_seg/sfreq} secs')
    ax.set_ylabel('Power V^2')
    
    
    fig.legend()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.xticks(ticks/5)
    plt.show()

#%% spectrogtram  of the 
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib.cm as cm

filt = filtered_data.get_data()[[0,1,2,5,6],:]


fig, axs = plt.subplots(nrows=len(filt), sharex=True)
fig.suptitle('Spectrograms of all channels')
cmap = cm.get_cmap('inferno') 

for ch, ax in zip(range(len(filt)), axs.ravel()):
   # x = filtered_data.get_data()[ch,:]
    x = filt[ch,:]

    f, t, Sxx = signal.spectrogram(x ,sfreq, nfft=512)
    mesh = ax.pcolormesh(t, f[0:80], Sxx[0:80,:], cmap=cmap,vmax=1e-11 , vmin=0.25e-12) #, vmax=Sxx.max()/100,vmin=Sxx.min()*100
    ax.set_ylabel(f'{layout[ch]}')
    ax.set_xlabel('Time [sec]')


fig.colorbar(mesh, ax= axs)
plt.xticks(ticks)

plt.show()

#%% PPG 
import numpy as np
import peak_detection_tools as peak
import feature_extraction_tools as feat

fs = 64
ch_to_compare = 0
features_fd=[[],[]]
features_td=[[],[]]
features_nl=[[],[]]


for idx, ppg_sig in enumerate([ppg1_data[ch_to_compare],ppg2_data[ch_to_compare]]):
    peaklist = peak.threshold_peakdetection(ppg_sig, fs)
    RR_list_e, RR_diff, RR_sqdiff = feat.calc_RRI(peaklist, fs)
    
    
    features_fd[idx] = feat.calc_fd_hrv(RR_list_e)
    features_td[idx] = feat.calc_td_hrv(RR_list_e, RR_diff, RR_sqdiff, window_length=60)
    features_nl[idx] = feat.calc_nonli_hrv(RR_list_e)
