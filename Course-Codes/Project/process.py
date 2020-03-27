# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 20:50:01 2020

@author: shaox16
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fftpack
import pandas as pd
import mne
from orderedset import OrderedSet
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

import utils


path = './data01'

fs, data = utils.load_continuous(path)
timestamp = utils.load_timestamps(path, fs)
event_labels = utils.load_event_labels(path)
print(event_labels.shape)
target_string = ('A', 'H', 'O', 'V', '2', '9', 'F', 'K', 'P', 'U', 'Z', '4')
# repetition times of each target
n_rep = 10
# Now plot it.
data.iloc[:, :20000].T.plot()

# design a filter
b = signal.firwin(1201, (1, 20), fs=fs, pass_zero=False)
# plot it 
fig = plt.figure()
w, h = signal.freqz(b, worN=1024)
#plt.plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
#plt.ylabel('Amplitude [dB]')
#plt.xlabel('Frequency [Hz]')
#plt.grid(linestyle=':')
#plt.xlim([0, 25])
#plt.ylim([-20, 1])
#plt.title('Frequency response of designed FIR digital filter')
#plt.show()

# filter data
filtered_data = data.apply(lambda x: signal.filtfilt(b, 1, x), axis=1, result_type='broadcast')
filtered_data.iloc[:, 10000:20000].T.plot(layout=(4, 2), subplots=True, figsize=(15, 10))

epoch = utils.cut_epochs((-0.2, 0.6, fs), filtered_data.values, timestamp)
epoch = utils.sort_epochs(epoch, event_labels)
labels = utils.get_label_bidir(target_string, n_rep, events=event_labels).flatten()

epoch = signal.detrend(epoch, axis=-1)
epoch = utils.apply_baseline((-0.2, 0.6, fs), epoch)

def plot_erp(t, y, epochs):
    ch_name = data.index.values.tolist()
    ch_order = ('P3', 'P7', 'O1', 'Oz', 'P4', 'P8', 'O2', 'Pz')
    ylim = np.max(np.abs(np.mean(epochs[y > 0], axis=0))) + 0.5
    
    fig, axes = plt.subplots(4, 2, figsize=(15, 15))
    for j in range(2):
        for i in range(4):
            ch = j * 4 + i
            ch_ind = ch_name.index(ch_order[ch])
            plt.ylim([-ylim, ylim])
            plt.xlim([t[0], t[-1]])
            # nontarget
            line1, = axes[i, j].plot(t, epochs[y == 0, ch_ind].mean(axis=0), c='gray', label='non-target')
            # left
            line2, = axes[i, j].plot(t, epochs[y == 1, ch_ind].mean(axis=0), label='leftward')
            # right
            line3, = axes[i, j].plot(t, epochs[y == 2, ch_ind].mean(axis=0), label='rightward')
            axes[i, j].set_title(ch_order[ch], fontsize=16)
    axes[0, 0].legend(fontsize=16)
    return fig

t = np.linspace(-0.2, 0.6, epoch.shape[-1])
fig = plot_erp(t, labels, epoch)
#plt.show()
fs_down = 40
epoch_cls = epoch[:, :, ::(fs  // fs_down)].copy()
t = np.linspace(-0.2, 0.6, epoch_cls.shape[-1])
fig = plot_erp(t, labels, epoch_cls)
plt.show()

def plot_concat(t, y, epochs):
    ylim = np.max(np.abs(np.mean(epochs[y > 0], axis=0))) + 0.5
    
    fig = plt.figure
    plt.ylim([-ylim, ylim])
    plt.xlim([t[0], t[-1]])
    # nontarget
    line1, = plt.plot(t, epochs[y == 0].mean(axis=0), c='gray', label='non-target')
    # left
    line2, = plt.plot(t, epochs[y == 1].mean(axis=0), label='leftward')
    # right
    line3, = plt.plot(t, epochs[y == 2].mean(axis=0), label='rightward')
    return fig
epoch_pro=epoch_cls[:,:,8:28]
epoch_pro=epoch_pro.reshape(720,-1)
t = np.linspace(0, 4, epoch_pro.shape[-1])
fig = plot_concat(t, labels, epoch_pro)
plt.show()

pca = PCA(n_components=5, svd_solver='randomized',
          whiten=True).fit(epoch_pro)
epoch_5d = pca.transform(epoch_pro)

param_grid = {'C': [1e5],
              'gamma': [0.1], }
#param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
#              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'),
                   param_grid, cv=5, iid=False)
clf = clf.fit(epoch_5d, labels)
y_pred = clf.predict(epoch_5d)

print(classification_report(labels, y_pred))
print(clf.best_estimator_)

path = './data02'

fs, data = utils.load_continuous(path)
timestamp = utils.load_timestamps(path, fs)
event_labels = utils.load_event_labels(path)
print(event_labels.shape)
target_string = ('A', 'H', 'O', 'V', '2', '9', 'F', 'K', 'P', 'U', 'Z', '4')
# repetition times of each target
n_rep = 10
# Now plot it.
data.iloc[:, :20000].T.plot()

# design a filter
b = signal.firwin(1201, (1, 20), fs=fs, pass_zero=False)
# plot it 
fig = plt.figure()
w, h = signal.freqz(b, worN=1024)
#plt.plot(w / np.pi * fs / 2, 20 * np.log10(np.abs(h)))
#plt.ylabel('Amplitude [dB]')
#plt.xlabel('Frequency [Hz]')
#plt.grid(linestyle=':')
#plt.xlim([0, 25])
#plt.ylim([-20, 1])
#plt.title('Frequency response of designed FIR digital filter')
#plt.show()

# filter data
filtered_data = data.apply(lambda x: signal.filtfilt(b, 1, x), axis=1, result_type='broadcast')
filtered_data.iloc[:, 10000:20000].T.plot(layout=(4, 2), subplots=True, figsize=(15, 10))

epoch = utils.cut_epochs((-0.2, 0.6, fs), filtered_data.values, timestamp)
epoch = utils.sort_epochs(epoch, event_labels)
labels = utils.get_label_bidir(target_string, n_rep, events=event_labels).flatten()

epoch = signal.detrend(epoch, axis=-1)
epoch = utils.apply_baseline((-0.2, 0.6, fs), epoch)

def plot_erp(t, y, epochs):
    ch_name = data.index.values.tolist()
    ch_order = ('P3', 'P7', 'O1', 'Oz', 'P4', 'P8', 'O2', 'Pz')
    ylim = np.max(np.abs(np.mean(epochs[y > 0], axis=0))) + 0.5
    
    fig, axes = plt.subplots(4, 2, figsize=(15, 15))
    for j in range(2):
        for i in range(4):
            ch = j * 4 + i
            ch_ind = ch_name.index(ch_order[ch])
            plt.ylim([-ylim, ylim])
            plt.xlim([t[0], t[-1]])
            # nontarget
            line1, = axes[i, j].plot(t, epochs[y == 0, ch_ind].mean(axis=0), c='gray', label='non-target')
            # left
            line2, = axes[i, j].plot(t, epochs[y == 1, ch_ind].mean(axis=0), label='leftward')
            # right
            line3, = axes[i, j].plot(t, epochs[y == 2, ch_ind].mean(axis=0), label='rightward')
            axes[i, j].set_title(ch_order[ch], fontsize=16)
    axes[0, 0].legend(fontsize=16)
    return fig

t = np.linspace(-0.2, 0.6, epoch.shape[-1])
fig = plot_erp(t, labels, epoch)
#plt.show()
fs_down = 40
epoch_cls = epoch[:, :, ::(fs  // fs_down)].copy()
t = np.linspace(-0.2, 0.6, epoch_cls.shape[-1])
fig = plot_erp(t, labels, epoch_cls)
plt.show()

#select a time window of 0-500ms
epoch_pro=epoch_cls[:,:,8:28]
#concatenate all 8 channels
epoch_pro=epoch_pro.reshape(720,-1)

pca = PCA(n_components=5, svd_solver='randomized',
          whiten=True).fit(epoch_pro)
epoch_5d = pca.transform(epoch_pro)
y_pred = clf.predict(epoch_5d)

print(classification_report(labels, y_pred))