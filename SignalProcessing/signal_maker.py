#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Generator of an acoustic signal with random frequencies taken from the Dataset.
"""

# Standard library imports
import argparse
import json
import os

# Third party imports
from matplotlib import pyplot as plt
import numpy as np

# Local application imports
from dsip import sigproc as dsp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True,
                    help="path to the input JSON file")
    args = vars(ap.parse_args())
    input_path = ''

    if args['file'].endswith('.json') and os.path.exists(args['file']):
        input_path = args['file']
    else:
        print('ERROR! JSON file not found.')
        os.sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    # PARAMETERS
    Fs = 48000
    length_bubble = 4500
    Ts = 1 / Fs
    bub_time = np.arange(0, length_bubble / Fs, Ts)

    # CREATE BUBBLES FROM RANDOM VALUES TAKEN IN EACH STAGE
    bubbles = []
    freqs_per_stage = [150, 500, 350]
    total_freqs = sum(freqs_per_stage)
    for i, n_freqs in enumerate(freqs_per_stage):
        stage = np.asarray(dsp.create_random_stage(dataset[i], n_freqs)).T
        for values in stage:
            freq, amplitude, vol, delta = values
            bubbles.append(dsp.create_signal(freq, delta, bub_time, amplitude))

    # CREATE THE SIGNAL VECTOR
    length_signal = Fs * 10
    signal = np.random.standard_normal(size=length_signal)
    time = np.arange(0, len(signal) / Fs, Ts)

    # REPLACING BUBBLES IN THE SIGNAL
    high_value = (length_signal - length_bubble) / Fs
    instants = np.random.uniform(0, high_value, size=total_freqs)

    for i, item in enumerate(instants):
        t = int(Fs * item)
        signal[t: t + length_bubble] += np.asarray(bubbles[i])

    # SHOW THE SIGNAL
    plt.figure()
    dsp.plot_signal(signal, time, 0)

    plt.figure()
    dsp.plot_spectrogram(signal, Fs, 0)

    plt.show()
