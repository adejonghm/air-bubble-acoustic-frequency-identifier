#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------


"""

# Standard library imports

# Third party imports
import numpy as np

# Local application imports
from dsip import sigproc as dsp

if __name__ == "__main__":

    # CREATING A SIGNAL
    Fs = 48000
    length = 4500
    Ts = 1 / Fs
    short_time = np.arange(0, length / Fs, Ts)

    signal_aa = dsp.create_signal(714, 0.08821, short_time, 3727.213)
    signal_ab = dsp.create_signal(725, 0.05851, short_time, 3693.755)

    signal_ba = dsp.create_signal(970, 0.02584, short_time, 1149.612)
    signal_bb = dsp.create_signal(832, 0.02782, short_time, 1505.294)
    signal_bc = dsp.create_signal(864, 0.02881, short_time, 1022.826)
    signal_bd = dsp.create_signal(1056, 0.05455, short_time, 844.906)

    signal_ca = dsp.create_signal(1109, 0.03673, short_time, 1086.202)
    signal_cb = dsp.create_signal(1120, 0.04366, short_time, 1120.07)
    signal_cc = dsp.create_signal(1141, 0.04069, short_time, 1064.270)

    start = np.zeros(Fs, dtype=float)
    subtotal = len(start) + length

    fill_1_2 = np.zeros(int(Fs * 1.9) - subtotal, dtype=float)
    subtotal += len(fill_1_2) + length

    fill_2_3 = np.zeros(int(Fs * 2.7) - subtotal, dtype=float)
    subtotal += len(fill_2_3) + length

    fill_3_4 = np.zeros(int(Fs * 3.2) - subtotal, dtype=float)
    subtotal += len(fill_3_4) + length

    fill_4_5 = np.zeros(int(Fs * 3.5) - subtotal, dtype=float)
    subtotal += len(fill_4_5) + length

    fill_5_6 = np.zeros(int(Fs * 4.3) - subtotal, dtype=float)
    subtotal += len(fill_5_6) + length

    fill_6_7 = np.zeros(int(Fs * 5.0) - subtotal, dtype=float)
    subtotal += len(fill_6_7) + length

    fill_7_8 = np.zeros(int(Fs * 5.4) - subtotal, dtype=float)
    subtotal += len(fill_7_8) + length

    fill_8_9 = np.zeros(int(Fs * 5.5) - subtotal, dtype=float)
    subtotal += len(fill_8_9) + length

    signal = np.concatenate((start, signal_aa, fill_1_2, signal_ba, fill_2_3, signal_ca, fill_3_4,
                             signal_ab, fill_4_5, signal_cb, fill_5_6, signal_bb, fill_6_7,
                             signal_bc, fill_7_8, signal_cc, fill_8_9, signal_bd))
    time = np.arange(0, len(signal) / Fs, Ts)

    noise = np.cos(2 * np.pi * 10 * time)
    signal += noise

    np.savetxt('signal_1.csv', signal, fmt='%f', delimiter=',')
