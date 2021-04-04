#!/usr/bin/env python3
# type: ignore

"""
Dev: 	adejonghm
----------

Used to separate each bubble that appears in the analyzed acoustic signal,
in independent acoustic signals.
"""


# Standard library imports
import os
import json
import argparse

# Third party imports
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

# Local application imports
import dsip.sigproc as dsp


# Setting Plot parameters
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['figure.figsize'] = (11, 6)
plt.rcParams['font.size'] = 10


if __name__ == "__main__":

    #### CONSTRUCT ARGUMENT PARSE ####
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

    # .:: GETTING JSON DATA ::.
    path = dataset[0]['path']

    # number of samples of a bubble
    size = dataset[0]['bubbleLength']

    # selecting the element in the JSON
    element = dataset[3]

    # path of the audio file
    # audio_path = path + element['path'] + element['audioName']
    audio_path = path + element['path'] + element['audioCutted']

    # .:: LOADING AUDIO FILE ::.
    Fs, wave = wavfile.read(audio_path)

    # .:: CUTTING SIGNAL THAT MATCHES THE VIDEO ::.
    # max_values = dsp.get_max_values(wave, size)
    # wave_cutted = wave[max_values[0]:max_values[-1]]

    # .:: FILTERING THE SIGNAL ::.
    sos = signal.butter(15, 500, 'hp', fs=Fs, output='sos')
    wave_filtered = signal.sosfilt(sos, wave)

    # .:: GETTING STAR OF EACH BUBBLE ::.
    points = np.array(dsp.get_max_values(wave_filtered, size, max_value=1000))
    points = points[1:-1]

    # correcting start bubble
    correction = 321
    start_points = points - correction

    plt.xlabel('Segundos (s)')
    plt.ylabel('Amplitude')
    plt.ylim(-6500, 6500)
    plt.plot(wave_filtered)
    for i, point in enumerate(start_points):
        plt.axvline(point, color='r', linestyle='--', alpha=0.5)
        plt.axvline(point + size, color='g', linestyle='--', alpha=0.5)
    for i, point in enumerate(points):
        plt.axvline(point, color='m', linestyle='--', alpha=0.5)
    plt.show()


#correction d6 = 321; max_value d6 = 1000;
