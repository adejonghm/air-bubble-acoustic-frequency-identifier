#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------


"""

# Third party imports
import numpy as np
from matplotlib import pyplot as plt

# Local application imports
from dsip import sigproc as dsp

if __name__ == "__main__":

    # PARAMETERS
    Fs = 48000
    bub_length = 4500
    Ts = 1 / Fs
    bub_time = np.arange(0, bub_length / Fs, Ts)

    ## CREATE THE BUBBLE SIGNALS
    bubbles = []
    bubbles.append(dsp.create_signal(714, 0.08821, bub_time, 3727.213))
    bubbles.append(dsp.create_signal(970, 0.02584, bub_time, 1149.612))
    bubbles.append(dsp.create_signal(1109, 0.03673, bub_time, 1086.202))
    bubbles.append(dsp.create_signal(725, 0.05851, bub_time, 3693.755))
    bubbles.append(dsp.create_signal(1120, 0.04366, bub_time, 1120.07))
    bubbles.append(dsp.create_signal(832, 0.02782, bub_time, 1505.294))
    bubbles.append(dsp.create_signal(864, 0.02881, bub_time, 1022.826))
    bubbles.append(dsp.create_signal(1141, 0.04069, bub_time, 1064.270))
    bubbles.append(dsp.create_signal(1056, 0.05455, bub_time, 844.906))

    ## CREATE THE SIGNAL VECTOR
    length_signal = int(Fs * 5.6)
    signal = np.random.standard_normal(size=length_signal)
    time = np.arange(0, len(signal) / Fs, Ts)

    ## REPLACING WITH THE SIGNAL
    instants = [1, 1.9, 2.7, 3.2, 3.5, 4.3, 5, 5.4, 5.5]
    for i, item in enumerate(instants):
        t = int(Fs * item)
        signal[t: t + bub_length] += bubbles[i]

    ## SAVE THE SIGNAL
    np.savetxt('signal_1.csv', signal, fmt='%f', delimiter=',')

    ## SHOW THE SIGNAL
    plt.figure()
    plt.plot(time, signal)
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.xticks(np.arange(0, 6, 0.5))

    plt.figure()
    plt.xlabel('Time (s)')
    plt.ylabel('Freq. [Hz]')
    plt.specgram(signal, Fs=Fs, cmap='jet')
    plt.ylim(0, 20000)
    cbar = plt.colorbar()
    # cbar.set_label('rel to.')

    plt.show()
