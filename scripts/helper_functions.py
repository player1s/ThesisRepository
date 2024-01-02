"""
Helper functions for analysis

- find nearest 
- eeg setup
- read psychopy file
- band power
- baseline correction
- remove dc component
- extract task segment
- get task duration
- extract data segment based on time range
- extract timestamp segment based on time range
- reject high amplitude epochs



Created on Thu Dec 21 10:46:28 2023

@author: elpid
"""

import numpy as np
import mne
import pandas as pd




def find_nearest(array, value):
    """
    Find the element in the ARRAY that is nearest to the VALUE.
    Return the array element and its index.
    """
    
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx] , idx



def eeg_setup (signal, fs ):
    """
    EEG settings on SIGNAL: montage, filtering BP: 1-50 Hz, notch: 50, 100Hz
    Return filtered data without bad channels (4,8) and info object.
    """
    
    layout = ["1", "2", "3", "4", "5", "6", "7", "8"]
    ch_types = ["eeg"] * 8
    sfreq = fs
    info = mne.create_info(layout, sfreq, ch_types)
    raw = mne.io.RawArray(signal, info)

    low_cut = 1
    high_cut = 50      
    filtered_data = raw.copy().filter(low_cut,high_cut,method='fir')
    notch_freqs = [50, 100]
    filtered_data = filtered_data.notch_filter(freqs=notch_freqs, filter_length='auto', method='fir')
    filtered_data.drop_channels(['4','8'])  
    
    return filtered_data, info



def psychopy_log(path, parameter):
    """
    Read phychopy csv file from PATH and return the PARAMETER in a pandas array.
    
    Parameters
    ----------
    path : str
    parameter : str

    Returns
    -------
    out: pandas array (without NaN).
    """
    
    data = pd.read_csv(path)
    out = data[parameter].dropna()    
    return out



def bandpower(data, sf, band, method='multitaper', window_sec=None, relative=False):
    """Compute the average power of the signal x in a specific frequency band.

    Requires MNE-Python >= 0.14.

    Parameters
    ----------
    data : 1d-array
      Input signal in the time-domain.
    sf : float
      Sampling frequency of the data.
    band : list
      Lower and upper frequencies of the band of interest.
    method : string
      Periodogram method: 'welch' or 'multitaper'
    window_sec : float
      Length of each window in seconds. Useful only if method == 'welch'.
      If None, window_sec = (1 / min(band)) * 2.
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
    from mne.time_frequency import psd_array_multitaper

    band = np.asarray(band)
    low, high = band

    # Compute the modified periodogram (Welch)
    if method == 'welch':
        if window_sec is not None:
            nperseg = window_sec * sf
        else:
            nperseg = (2 / low) * sf

        freqs, psd = welch(data, sf, nperseg=nperseg)

    elif method == 'multitaper':
        psd, freqs = psd_array_multitaper(data, sf, adaptive=True,
                                          normalization='full', verbose=0)

    # Frequency resolution
    freq_res = freqs[1] - freqs[0]

    # Find index of band in frequency vector
    idx_band = np.logical_and(freqs >= low, freqs <= high)

    # Integral approximation of the spectrum using parabola (Simpson's rule)
    bp = simps(psd[idx_band], dx=freq_res)

    if relative:
        bp /= simps(psd, dx=freq_res)
    return bp



def baseline_av(baseline, baseline_ts, details=False):
    """
    Segment the baseline period into 5 second epochs and return the average of them.
    Reject any epoch with amplitude higher than 100uV.

    Parameters
    ----------
    baseline : TYPE
        DESCRIPTION.
    baseline_ts : TYPE
        DESCRIPTION.
    details : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    baseline_average : TYPE
        DESCRIPTION.

    """

    baseline_epochs, baseline_epochs_ts, baseline_rejected_epochs = split_into_epochs_and_reject(baseline, baseline_ts, threshold=100e-6, epoch_length=5)
    baseline_average = np.mean(baseline_epochs, axis=0)

        
    if details == True:
        print(f'{len(baseline_rejected_epochs)} epochs were rejected from the baseline due to high amplitude.')    
    return baseline_average



def remove_dc(data):
    """
    Remove the DC component by removing the average value of each channel from
    the continuous data of the same channel.

    Parameters
    ----------
    data : numpy array (channels, time-points)

    Returns
    -------
    without_dc : numpy array (channels, time-points)

    """
    
    without_dc = np.zeros_like(data)
    for ch in range(0,len(data)):
        without_dc[ch] = data[ch,:] - data.mean(axis=1)[ch]        
    return without_dc



def extract_task_segments(task_id, data, timestamps, markers, markers_ts):
    """
    Extract segments for a specific task from the continuous data.

    Parameters
    ----------
    task_id : int
        Id of the task of the experiment.
    data : numpy array
        Continuous data from where the segment is extracted 
        (channels x timeseries).
    timestamps : numpy array
        Timestamps of the continous data.
    markers : numpy array
        Array of markers for all the tasks through the experiment.
    markers_ts : numpy aray
        Timestamps of the markers.

    Returns
    -------
    numpy array
        Segment from the continuous data of a specific task of the experiment.

    """
    
    task_segments = []
    task_timestamps = []
    start_indices = np.where(markers == task_id)[0]
    for start_index in start_indices:
        start_time = markers_ts[start_index]
        end_time = start_time + get_task_duration(task_id)
        if end_time > timestamps[-1]:
            # If the recording is cut short, take as end_time of the segment as the last timestamp
            end_time = timestamps[-1]
        segment = extract_segment(start_time, end_time, data, timestamps)
        task_segments.append(segment)

        segment_timestamps = extract_segment_timestamps(start_time, end_time, timestamps)
        task_timestamps.append(segment_timestamps)
    return np.concatenate(task_segments, axis=1), np.concatenate(task_timestamps)


def get_task_duration(task_id):
    """
    Returns the duration of each task based on the task id.

    Parameters
    ----------
    task_id : int
        Id of the task of the experiment.

    Returns
    -------
    int
        The duration of the task of the experiment in seconds.

    """
    durations = {
        1: 30,      # BASELINE SECTION LENGTH
        2: 150,     # PVT SECTION LENGTH
        4: 150,     # MATH SECTION LENGTH
        7: 300,   # TETRIS SECTION LENGTH
        11: 300   # SNAKE SECTION LENGTH
    }
    return durations.get(task_id, 0)



def extract_segment(start_time, end_time, data, timestamps):
    """
    Extract segment of the continuous data based on timestamps.
    Start_time & end_time should be in the same format/ units as timestamps.

    Parameters
    ----------
    start_time : float
        Start time for the segment to be extracted.
    end_time : float
        End time for the segment to be extracted.
    data : numpy array
        Continuous data from where the segment is extracted 
        (channels x timeseries).
    timestamps : numpy array
        Timestamps of the continous data.

    Returns
    -------
    numpy array
        Segment from the continuous data.

    """
    start_index = np.argmax(timestamps >= start_time)
    end_index = np.argmax(timestamps >= end_time)
    return data[:, start_index:end_index]



def extract_segment_timestamps(start_time, end_time, timestamps):
    """
    Extract segment timestamps based on time range.
    Start_time & end_time should be in the same format/ units as timestamps.


    Parameters
    ----------
    start_time : float
        Start time for the segment to be extracted.
    end_time : float
        End time for the segment to be extracted.
    timestamps : numpy array
        Timestamps array from which segment is to be extracted.

    Returns
    -------
    numpy array
        Segment from the timestamps data.

    """
    return timestamps[(timestamps >= start_time) & (timestamps < end_time)]



def reject_high_amplitude_epochs(data, timestamps):
    # Calculate peak-to-peak amplitudes for each epoch
    ptp_amplitudes = np.ptp(data, axis=2)

    # Find epochs with peak-to-peak amplitude greater than 100e-6
    high_amplitude_epochs = np.where(ptp_amplitudes > 100e-6)[0]

    # Remove corresponding sections from the timestamps array
    epochs, channels, timeseries = data.shape
    timestamps_rejected = np.delete(timestamps, high_amplitude_epochs * timeseries)

    # Remove epochs with high amplitudes from the EEG data
    eeg_data_rejected = np.delete(data, high_amplitude_epochs, axis=0)

    return eeg_data_rejected, timestamps_rejected



def split_into_epochs(data_array, timestamps, epoch_length=5):
    sample_rate = timestamps[-1] / (data_array.shape[1] - 1)  # Calculate sample rate

    # Calculate number of samples in each 5-second epoch
    samples_per_epoch = int(epoch_length * sample_rate)

    # Find the total number of epochs
    num_epochs = int(timestamps[-1] / epoch_length)

    epoch_data = []
    epoch_timestamps = []

    for i in range(num_epochs):
        start_time = i * epoch_length
        end_time = (i + 1) * epoch_length

        # Find indices corresponding to start and end times
        start_idx = np.argmax(timestamps >= start_time)
        end_idx = np.argmax(timestamps >= end_time) + 1

        # Ensure the epoch is within the bounds of the data
        if end_idx < data_array.shape[1]:
            epoch_data.append(data_array[:, start_idx:end_idx])
            epoch_timestamps.append(timestamps[start_idx:end_idx])

    return epoch_data, epoch_timestamps



def split_into_epochs_and_reject(data_array, timestamps, threshold=100e-6, epoch_length=5):
    sample_rate = 250  # Sampling frequency in Hz
    n_channels, data_length = data_array.shape

    # Calculate number of samples in each 5-second epoch
    samples_per_epoch = int(epoch_length * sample_rate)

    epoch_data = []
    epoch_timestamps = []
    rejected_epochs = []
    
    num_epochs = data_length // samples_per_epoch

    for i in range(num_epochs):
        start_idx = i * samples_per_epoch
        end_idx = start_idx + samples_per_epoch

        epoch_data_batch = []
        epoch_timestamps_batch = timestamps[start_idx:end_idx]
        

        for channel in range(n_channels):
            epoch = data_array[channel, start_idx:end_idx]
            ptp_amplitude = np.ptp(epoch)

            if ptp_amplitude <= threshold:
                epoch_data_batch.append(epoch)

        if len(epoch_data_batch) == n_channels:
            epoch_data.append(np.array(epoch_data_batch))
            epoch_timestamps.append(epoch_timestamps_batch)
        else:
            rejected_epochs.append(i)


    return epoch_data, epoch_timestamps, rejected_epochs