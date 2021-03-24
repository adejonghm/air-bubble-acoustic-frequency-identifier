#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Analyze the three acoustic signals obtained, for example, show the
average frequency of each acoustic signal, all in the same graph.
"""


# Standard library imports
import argparse
import json
import os

# Third party imports
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq

# Local application imports
import dsip.sigproc as dsp

# Setting Plot parameters
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['figure.figsize'] = (11, 6)
plt.rcParams['font.size'] = 8


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="path to the input JSON file")
    args = vars(ap.parse_args())

    if args['file'].endswith('.json') and os.path.exists(args['file']):
        input_path = args['file']
    else:
        print('ERROR! JSON file not found.')
        os.sys.exit(1)


    #### READ JSON FILE ####
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)
   
    for i in range(1, 4):
        f_axis = []
        frequencies = []
        node = dataset[i]
        audio_path = dataset[0]['path'] + node['path'] + node['audioCutted']
        beginnings = node['bubblesStart']
        size = dataset[0]['bubbleLength']
        diameter = node['diameter']
        Eo = node['Eotvös_Numbers']
        Re = node['Reynolds_Numbers']

        #### LOADING AUDIO FILE ####
        Fs, wave = wavfile.read(audio_path)

        #### FILTRANDO EL AUDIO ####
        sos = signal.butter(15, 500, 'hp', fs=Fs, output='sos')
        wave_filtered = signal.sosfilt(sos, wave)

        #### SETTING PARAMETERS ####
        total_bubbles = len(beginnings)
        Ts = 1 / Fs
        N = len(wave_filtered)
        half = N / 2

        for k in range(total_bubbles):
            bubble = dsp.get_bubble(wave_filtered, beginnings[k], size)
            bubble_length = len(bubble[0])
            f_axis = fftfreq(bubble_length) * Fs

            fast_fourier_transform = abs(fft(2 * bubble[0]) / bubble_length)
            position = fast_fourier_transform.tolist().index(max(fast_fourier_transform))

            freq = int(f_axis[position])
            radius = dsp.get_radius(freq)

            frequencies.append(fast_fourier_transform)

        #### MEAN FREQUENCIES ####
        mean = np.mean(frequencies, axis=0)
        v_max = mean.max()
        p_max = mean.tolist().index(v_max)
        f_max = f_axis[p_max]

        # plt.plot(f_axis, mean, marker='.', label='diâmetro do bocal: {} mm'.format(diameter))
        # plt.xlim(500, 1300)
        # plt.ylim(0, 550)
        # plt.text(f_max-10, v_max + 15, '{} Hz'.format(int(f_max)))
        # plt.text(f_max-1, v_max, '|')

        #### GRACE DIAGRAM ####
        plt.plot(Eo, Re, 'h', label='Nozzle - {}mm'.format(diameter))

    #### GRACE DIAGRAM ####
    plt.title("Grace Diagram")
    plt.xlabel('Eötvös Numbers (Eo)')
    plt.ylabel('Reynolds Numbers (Re)')

    #### MEAN FREQUENCIES ####
    # plt.title('Mean Frequency of each Acoustic Signal')
    # plt.xlabel('Frequency [Hz]')
    # plt.ylabel('Amplitude')

    plt.legend(loc='best')
    plt.show()
