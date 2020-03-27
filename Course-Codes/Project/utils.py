import os

import numpy as np
import pandas as pd
import pyedflib
from mne import baseline
from scipy.ndimage import convolve1d


######################################################################
# Data loader
######################################################################

def load_continuous(data_dir):
    """
    Neuracle bdf data loader
    :param data_dir:
    :return:
        samplerate, int
        raw data: pandas.DataFrame
    """
    file = os.path.join(data_dir, 'data.bdf')
    # read data
    f_data = pyedflib.EdfReader(file)
    ch_names = f_data.getSignalLabels()
    data = np.array([f_data.readSignal(i) for i in range(f_data.signals_in_file)])

    # sample frequiencies
    sfreq = f_data.getSampleFrequencies()
    assert np.unique(sfreq).size == 1
    print("Sample frequency: %d" % sfreq[0])

    return sfreq[0], pd.DataFrame(data, ch_names)


def load_timestamps(path, fs):
    file = os.path.join(path, 'evt.bdf')

    # read timestamp
    f_evt = pyedflib.EdfReader(file)
    timestamp, _, _ = f_evt.readAnnotations()
    timestamp = list(map(lambda x: int(x * fs), timestamp))

    return timestamp


def load_event_labels(path):
    file = os.path.join(path, 'order.txt')
    with open(file) as f:
        stim_order = [[int(x) for x in line.split()] for line in f if len(line) > 1]
    stim_order = np.asarray(stim_order, dtype=np.int32)
    stim_order = stim_order[:, ::2]
    return stim_order


######################################################################
# Epoch utils
######################################################################

def get_label_bidir(stim_string, n_rep, events):
    characters = list(range(65, 91)) + list(range(48, 58))
    keyboard = np.reshape(characters, (6, 6))
    st_order = np.sort(events, axis=-1)

    def is_target(num, order):
        assert 0 <= order < 12
        if order < 6:
            return num in keyboard[order]
        else:
            return num in keyboard[:, order - 6]

    string = []
    for c in stim_string:
        string.extend([c] * n_rep)
    label = []
    for i, c in enumerate(string):
        num = ord(c)
        for order in st_order[i]:
            if order in {3, 4, 5, 9, 10, 11}:
                left = is_target(num, order)
                right = is_target(num, order - 3)
            else:
                left = is_target(num, order)
                right = is_target(num, order + 3)
            if not left and not right:
                label.append(0)
            elif left:
                label.append(1)
            elif right:
                label.append(2)
            else:
                raise ValueError('Left and right are both target: impossible')
    return np.array(label)



def cut_epochs(t, data, timestamps):
    """
    cutting raw data into epochs based on event timestamps
    :param t time: tuple (start, end, samplerate)
    :param data: ndarray (n_channels, n_times)
    :param timestamps: list of timestamps
    :return: ndarray (n_epochs, n_channels, n_times)
    """
    assert data.ndim == 2
    timestamps = np.array(timestamps)
    start = timestamps + int(t[0] * t[2])
    end = timestamps + int(t[1] * t[2])
    epochs = np.stack([data[:, s:e] for s, e in zip(start, end)], axis=0)
    return epochs


def sort_epochs(epochs, event):
    """
    sorting epoch data according to event labels
    :param epochs: 3d epochs (n_epochs, n_channels, time_seq)
    :param event: 2d event array (n_trials, 12)
    :return:
        sorted_epochs: ndarray, with the same shape of "epochs"
    """
    assert epochs.ndim == 3
    rep_dim = event.shape[1]
    indices = np.argsort(event, axis=-1).flatten()
    for i in range(0, indices.shape[0], rep_dim):
        indices[i:i + rep_dim] += i
    sorted_epochs = epochs[indices]  # fancy index
    return sorted_epochs


######################################################################
# Signal processing utils
######################################################################

# apply_baseline use mne.
def apply_baseline(t, data, mode='mean'):
    """
    Simple wrapper for mne.baseline.rescale
    :param t: tuple (start, end, samplerate)
    :param data: ndarray of any shape with axis=-1 the time axis
    :param mode: 'mean' | 'ratio' | 'logratio' | 'percent' | 'zscore' | 'zlogratio'
        refer to mne.baseline.rescale
    :return: ndarray
    """
    start, end, samplerate = t
    base = (start, 0)
    times = np.linspace(start, end, data.shape[-1])
    data = baseline.rescale(data, times, baseline=base, mode=mode, verbose=False)
    return data


def _average(data, n=3, axis=0):
    """
    # moving window average along epochs
    :param data: ndarray, the first dimension the epoch count
    :param n: average n epochs
    :param axis: axis to take average
    :return:
    """
    kernel = np.ones((n,)) / n
    mean_resp = convolve1d(data, kernel, axis=axis, mode='reflect')
    return mean_resp


def average_multiclass(data, labels, n=3):
    """
    take average for multiclass epoch data or output scores of classifier
    :param data: epoch data with shape (n_epochs, n_channels, n_time)
    :param labels: label of epoch data
    :param n: times of epoch averaging
    :return:
    """
    # map labels
    uni_label = np.unique(labels)
    book_list = [labels == i for i in uni_label]
    x_list = [data[book] for book in book_list]

    # map average function
    data_list = list(map(lambda x: _average(x, n), x_list))
    # reshape
    mean_resp = np.zeros_like(data)
    for i, book in enumerate(book_list):
        mean_resp[book] = data_list[i]
    return mean_resp


######################################################################
# Evaluation utils
######################################################################

def itr(p, n, t):
    """
    information transfer rate in bits/min
    :param p: accuracy 
    :param n: number of targets
    :param t: average information transfer time[s] (average time required for single time decision making)
    """
    trans = np.log2(n)
    if 0 < p < 1:
        loss = p * np.log2(p) + (1 - p) * np.log2((1 - p) / (n - 1))
    elif p == 0:
        loss = -trans
    else:
        loss = 0
    it = trans + loss
    return it / t * 60
