#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

It is used to calculate the decay of the acoustic signal of a bubble.
"""

# Standard library imports
import argparse
import json
import os

# Third party imports
import numpy as np
from scipy import signal
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
from matplotlib import pyplot as plt

# Local application imports


if __name__ == '__main__':

    #### CONSTRUCT ARGUMENT PARSE ####
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True,
                    help="path to the input JSON file")
    args = vars(ap.parse_args())

    if args['file'].endswith('.json') and os.path.exists(args['file']):
        input_path = args['file']
    else:
        print('ERROR! JSON file not found.')
        os.sys.exit(1)

    #### READ JSON FILE ####
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    #### LOADING JSON DATA ####
    # general data
    db_path = dataset[0]['path']
    bub_length = dataset[0]['bubbleLength']

    # node data
    node = dataset[3]
    node_path = db_path + node['path']
    diameter = node['diameter']
    bub_beginnings = node['bubblesStart']
    audio_path = node_path + node['audioCutted']

    #### LOADING AUDIO FILE ####
    Fs, wave = wavfile.read(audio_path)

    #### FILTERING THE SIGNAL ####
    sos = signal.butter(15, (500, 1500), 'bandpass', fs=Fs, output='sos')
    wave_filtered = signal.sosfilt(sos, wave)

    #### READ THE BUBBLE SIGNAL
    start = bub_beginnings[5]
    end = start + bub_length
    bub_signal = wave_filtered[start:end]

    #### CREATE TIME VECTOR
    Ts = 1 / Fs
    amp_max = np.max(bub_signal)
    t_min = np.where(bub_signal == amp_max)[0][0]
    t_max = 2800
    real_signal = bub_signal[t_min:t_max]
    signal_length = len(real_signal)
    t = np.arange(0, signal_length / Fs, Ts)
    delta_t = (t_max - t_min) / signal_length

    ### FREQUENCY OF THE SIGNAL
    fast_fourier_transform = abs(fft(2 * bub_signal) / len(bub_signal))
    position = np.where(fast_fourier_transform == max(fast_fourier_transform))[0][0]
    f_axis = fftfreq(len(bub_signal)) * Fs
    f = f_axis[position]
    omega = f * 2 * np.pi

    #### CREATE LAMBDA VECTOR
    lmda_min = 0.01
    lmda_max = 1
    lmda_length = 1000
    lmda = lmda_min
    delta_lmda = (lmda_max - lmda_min) / lmda_length

    q_error = np.zeros(lmda_length)

    #### LOOKING FOR EFFECTIVE LAMBDA
    for i in range(lmda_length):
        x = amp_max * np.cos(omega * t) * np.exp(-np.pi * lmda * f * t)
        q_diff = np.power(real_signal - x, 2)
        q_error[i] = np.sum(q_diff)
        lmda = lmda_min + i * delta_lmda

    minimal_error = np.min(q_error)
    index = np.where(q_error == minimal_error)[0][0]
    lmda_effective = lmda_min + index * delta_lmda
    print('effective lambda:', lmda_effective)

    #### CREATING THE IDEAL SIGNAL WITH THE EFFECTIVE LAMBDA
    ideal_signal = amp_max * np.cos(omega * t) * np.exp(-np.pi * lmda_effective * f * t)

    #### PLOTTING THE SIGNAL
    plt.figure()
    plt.plot(t, real_signal, linewidth=1, label='real')

    plt.title('Signal')
    plt.plot(t, ideal_signal, linewidth=1, label=f'ideal, with delta={lmda_effective}')
    plt.xlabel('Seconds')
    plt.legend()

    plt.figure()
    plt.plot(f_axis, fast_fourier_transform)
    plt.xlim(0, 3000)
    plt.xlabel('Frequency [Hz]')

    plt.show()
