#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------


"""

# Standard library imports
import argparse
# import sys

# Third party imports
import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, fftfreq

# Local application imports
from dsip import sigproc as dsp


if __name__ == "__main__":

    #### CONSTRUCT ARGUMENT PARSE ####
    ap = argparse.ArgumentParser()
    ap.add_argument("--option", required=False,
                    help="use the option (--option plot) to display the plots.")
    args = vars(ap.parse_args())

    signal = np.loadtxt('signal_1.csv')
    vol = 0
    Fs = 48000
    frequencies = []
    bubble_length = 4500
    time = len(signal) / Fs

    peaks = dsp.get_peaks(signal, bubble_length, max_value=800)

    for i, peak in enumerate(peaks):
        bubble, _ = dsp.get_bubble(signal, peak, bubble_length, fs=Fs)
        fast_fourier_transform = abs(fft(2 * bubble) / bubble_length)
        position = np.where(fast_fourier_transform ==
                            max(fast_fourier_transform))
        f_axis = fftfreq(bubble_length) * Fs
        freq = int(f_axis[position[0][0]])
        frequencies.append(freq)

        # radius in mm
        r = dsp.get_radius(freq) * 1000

        # volume in mm^3
        vol += (4 * np.pi * np.power(r, 3)) / 3

        plt.plot(f_axis, fast_fourier_transform,
                 marker='.', label='{} Hz'.format(freq))
        plt.xlim(500, 1500)


    scenarios = dsp.frequency_classifier(frequencies)
    print('Leak = {} mm³/s'.format(np.round(vol / time, 2)))
    print('Scenario |', 'Bubbles')
    print('-' * 18)
    for i, item in enumerate(scenarios):
        print(' '*3, f'{1 + i}', ' '*2, '|', ' '*2, f'{item}')

    plt.legend(loc='upper right')
    plt.xlabel('Freq. [Hz]')
    plt.ylabel('Amplitude')

    plt.figure()
    plt.xlabel('Time (s)')
    plt.ylabel('Freq. [Hz]')
    plt.specgram(signal, Fs=Fs, cmap='jet')
    plt.ylim(0, 20000)
    plt.colorbar()
    # cbar = plt.colorbar()
    # cbar.set_label('rel to.')
    plt.show()
