#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Classifier:
    script to detect the fundamental frequencies of an acoustic signal and classify it
    according to its size.

"""

# Standard library imports
import argparse
import sys

# Third party imports
import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, fftfreq

# Local application imports
from dsip import sigproc as dsp


def classifier(freqs: list) -> list:
    """
    Function to classify the existing frequencies in the acoustic signal.
    """
    c1 = 0
    c2 = 0
    c3 = 0

    for f in freqs:
        if 700 < f < 800:
            c1 += 1
        elif 800 < f < 1100:
            c2 += 1
        elif 1100 < f < 1200:
            c3 += 1

    return [c1, c2, c3]


if __name__ == "__main__":

    #### CONSTRUCT ARGUMENT PARSE ####
    ap = argparse.ArgumentParser()
    ap.add_argument("--option", required=False,
                    help="use the option (--option plot) to display the plots.")
    args = vars(ap.parse_args())

    # CREATING A SIGNAL
    Fs = 48000
    length = 4500
    Ts = 1 / Fs
    time = np.arange(0, length / Fs, Ts)

    signal_a = dsp.create_signal(714, 0.08821, time, 3727.213)
    signal_b = dsp.create_signal(970, 0.02584, time, 1149.612)
    signal_c = dsp.create_signal(1109, 0.03673, time, 1086.202)
    signal_d = dsp.create_signal(928, 0.02584, time, 1082.014)

    signal = signal_a + signal_b + signal_c + signal_d

    fast_fourier_transform = abs(fft(2 * signal) / len(signal))
    f_axis = fftfreq(len(signal)) * Fs

    n_fft = len(fast_fourier_transform) // 2
    max_values_positions = []
    value = 0
    flag = True

    for i in range(n_fft):
        item = fast_fourier_transform[i]
        next_item = fast_fourier_transform[i + 1]
        if flag:
            if item < next_item:
                value = next_item
            else:
                max_values_positions.append(i)
                flag = False
        else:
            if item > next_item:
                value = 0
            else:
                flag = True
    frequencies = [int(f_axis[i]) for i in max_values_positions]
    bub_by_scen = classifier(frequencies)

    if args['option'] is None:
        print('----' * 8)
        print(' ' * 12, 'Total Bubbles')
        print('----' * 8)
        print('Scenario #1 \t {}'.format(bub_by_scen[0]))
        print('----' * 8)
        print('Scenario #2 \t {}'.format(bub_by_scen[1]))
        print('----' * 8)
        print('Scenario #3 \t {}'.format(bub_by_scen[2]))
        print('----' * 8)
        print('* You can use "--option plot" to display the FFT graph.')
    elif args['option'] == 'plot':
        plt.xlabel('Freq. [Hz]')
        plt.ylabel('Amplitude')
        plt.xlim(0, 4000)
        plt.yticks(np.arange(0, 270, 25))
        plt.plot(f_axis, fast_fourier_transform,
                 linewidth=0.8)  # , marker='.')

        # start = np.zeros(500, dtype=float)

        # long_signal = np.concatenate((start, signal), axis=None)
        # long_time = np.arange(0, len(long_signal)) / Fs

        # plt.xlabel('Seg.')
        # plt.ylabel('Amplitude')
        # plt.plot(long_time, long_signal)
        plt.show()
    else:
        print('Use --help to show options or not use any option')
        sys.exit(1)
