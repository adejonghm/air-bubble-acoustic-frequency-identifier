#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Generator of an acoustic signal with random frequencies and its respective values.
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
    bub_length = 4500
    Ts = 1 / Fs
    bub_time = np.arange(0, bub_length / Fs, Ts)

    # CREATE THE BUBBLE SIGNALS
    bubbles = []
    stage = np.asarray(dsp.create_random_stage(dataset[0], 9)).T
    for values in stage:
        freq, amplitude, vol, delta = values
        bubbles.append(dsp.create_signal(freq, delta, bub_time, amplitude))

    # CREATE THE SIGNAL VECTOR
    length_signal = int(Fs * 5.6)
    signal = np.random.standard_normal(size=length_signal)
    time = np.arange(0, len(signal) / Fs, Ts)

    # REPLACING WITH THE SIGNAL
    instants = np.random.uniform(0, 5.6, size=9)

    for i, item in enumerate(instants):
        t = int(Fs * item)
        signal[t: t + bub_length] += bubbles[i]

    # SHOW THE SIGNAL
    plt.figure()
    plt.plot(time, signal)
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.xticks(np.arange(0, 6, 0.5))

    plt.show()
