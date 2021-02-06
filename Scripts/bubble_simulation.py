#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

MATHEMATICAL MODEL PROPOSED BY STRASBERG IN 1956
"""

# Standard library imports
from math import pi

# Third party imports
import numpy as np
import matplotlib.pyplot as plt



# .: Parameters :.
# Distance from the center of the bubble.(m)
d = 1

# Sampling Frequency. (puntos/seg)
Fs = 10000

# Atmospheric pressure (Pa). Taking it as initial pressure (P0)
atm_pressure = 101325

# Specific Heat Radio. (gamma = k = Cp/Cv)
gamma = 1.40

# Frequency en Hz.
freq = 610

# Liquid Water Density (rho). Expressed in (Kg/m^3)
rho = 998

# Maximun Time. (seg)
tmax = 0.2

# Number of points.
N = Fs * tmax

# Time
t = np.arange(0, N) / Fs

# Initial radius of the bubble (R_0). Expressed in meters (m)
# radio = 0.0033

# Water Column Depth in (m)
# h = 3

# Gravitational acceleration in (m/s^2)
# g = 9.98

# .:: Calculating The Frequency (Minnaert) ::.
# Po = atm_pressure + rho * g * h
radio = ((3 * gamma * atm_pressure / rho) ** (1/2)) / (2 * pi * freq)


# .:: Calculating the Sound Pressure Amplitude ::.
# Value obtained by clearing P+ in the equation
# to calculate Sound pressure amplitude. (1,09 x 10^-4)
# eP = termino1 = (1 / (2 * gamma * atm_pressure)) * ((0.03 * d) / radio) ** 2
eP = 1.09 * (10**-4)

# p0 = (radio / d) * (2 * gamma * Po * eP) ** (1/2)
p0 = (radio / d) * (2 * gamma * atm_pressure * eP) ** (1/2)


# .:: Calculating the Sound Pressure ::.
delta = 0.014 + 1.1 * 10**-5 * freq
e = np.exp(-pi * delta * freq * t)
cos = np.cos(2 * pi * freq * t)
ps = p0 * e * cos


# Adding noise to the signal
noise = np.cos(2*pi*30*t)
Ps = ps * noise

start = np.zeros(500, dtype=float)
Ps1 = np.concatenate((start, Ps), axis=None)
length = len(start) + len(t)
t1 = np.arange(0, length) / 10000

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
# ax1.set_title('Audio Signal')
# ax1.set_xlabel('Time [ms]')
# ax1.set_ylabel('Amplitude')
# ax1.plot(Ps1)

# ax2.specgram(Ps, Fs=Fs)
# ax2.set_title('Spectrogram')
# ax2.set_xlabel('Time [s]')
# ax2.set_ylabel('Frequency [Hz]')
# ax2.set_ylim(0, 3000)

plt.figure(figsize=(20, 10))
plt.rcParams.update({'font.size': 16})
# plt.title('Audio Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [Pa]')
plt.plot(t1, Ps1, 'blue')
# plt.xticks(np.arange(0, 220, 20))
# plt.xlim(0.10,0.30)
plt.show()

microbar = p0*10
print("Image Description:")
print("------------------")
print(" » Radius: %.1f[mm] \n » Frequency: %.0f[Hz]" %(radio * 1000, freq))
print(" » Amplitude: %.2f[Pa]" %(p0))
