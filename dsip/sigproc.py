#!/usr/bin/env python3

"""
Dev: 	adejonghm
----------

This module was implemented in order to create functions used in
the digital signal processing performed.
"""


# Standard library imports
import os
from math import pi

# Third party imports
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.io import wavfile
from tqdm import tqdm

# Local application imports


def clear():
    """Clear the terminal"""

    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def get_bubble(audio: np.ndarray, start: int, size: int, fs: int = 48000) -> tuple:
    """Selects a specific bubble of the audio, from its start and duration.

    Args:
        audio (np.ndarray): Acoustic signal from where the bubble will be obtained.
        start (int): Point where the bubble begins.
        size (int): Size of the bubble.
        fs (int, optional): Sampling frequency. Defaults to 48000.

    Returns:
        tuple: The signal and its time length.
    """

    bubble = audio[start: start + size]
    bubble_time = np.arange(0, len(bubble) / fs, 1/fs) * 1000

    return (bubble, bubble_time)


def get_max_values(audio: np.ndarray, size: int, max_value: int = 8000) -> list:
    """Determine the amplitude values that are higher than a given value,
    which will be taken as maximum amplitude values in the audio.

    Args:
        audio (np.ndarray): Acoustic signal in which the maximum values will be found.
        size (int): Size of the bubble.
        max_value (int, optional): The value taken as a threshold. Defaults to 8000.

    Returns:
        list: All the maximum values found.
    """

    max_pos = []
    for i in range(0, len(audio), size):
        chunk = audio[i:i+size]
        m = chunk.max()
        if m > max_value:
            max_pos.append(audio.tolist().index(m))
    return max_pos


def get_radius(frequency: int) -> float:
    """Mathematical model proposed by Minnaert to determine
    the natural frequency of the acoustic emission of a bubble.

    Args:
        frequency (int): Frequency of the bubble

    Returns:
        float: Radius of the bubble in meters
    """

    # Specific Heat Radio. (k = Cp/Cv)
    specific_heat_ratio = 1.40

    # Liquid Water Density (rho). Expressed in [Kg/m^3]
    rho = 998

    # Atmospheric pressure taking it as initial pressure [Pa]
    atm_pressure = 101325

    return ((3 * specific_heat_ratio * atm_pressure / rho) ** (1/2)) / (2 * pi * frequency)


def get_eotvos(radius: float) -> float:
    """Find the Eötvös Number of a Bubble: (Δρ·g·d^2) / σ

    (Δrho) : Water Density - Air Density
    (g): The Gravitational Aceleration.
    (d^2): The diameter of the Bubble.
    (sigma) : The surface tension of the liquid.

    Args:
        radius (float): Radius of the bubble

    Returns:
        float: The Eötvös number of the bubble
    """

    delta_rho = 997
    gravity = 9.8
    liquid_surface_tension = 7.6e-2

    return (delta_rho * gravity * pow(radius*2, 2)) / liquid_surface_tension


def get_reynolds(radius: float, v_rel: float, scale_factor: float = 0.3846) -> float:
    """Find the Reynolds Number of a Bubble: (ρ·Vr·d) / μ

    (rho): The Water Density. [Kg/m^3]
    (Vr): Relative Velocity = Air Velocity (Deformation Velocity) - Liquid Velocity
    (d): The diameter of the Bubble.
    (mu): The Dynamic Viscosity of the Liquid. [Pa·s]

    Args:
        radius (float): Radius of the bubble.
        v_rel (float): Relative Velocity.
        scale_factor (float): Convection value of 1 pixel in millimeters (0.3846).

    Returns:
        float: The Reynolds number of the bubble.
    """

    rho = 998
    mu = 8.9e-4

    # speed_deformation * 1px en mm / 1000 -> para llevar a metros
    v_rel = v_rel * scale_factor * 1e-3

    return (rho * v_rel * radius * 2) / mu


def plot_signal(audio: np.ndarray, diameter: int, time: np.ndarray, *args):
    """Display an acoustic signal as a function of time.

    Args:
        audio (np.ndarray): Acoustic signal to be plotted.
        diameter (int): Diameter of the nozzle used in the title of the plot.
        time (np.ndarray): Time vector over which the acoustic signal is represented.
        *args[begs (list), Fs (int)]: 'Fs' is the sampling frequency and
                                      'begs' are the beginnings of the bubbles.
    """

    plt.title('Time Domain Signal [Diameter of nozzle: {} mm]'.
              format(diameter))
    plt.xlabel('Segundos (s)')
    plt.ylabel('Amplitude')
    plt.ylim(-4000, 4000)
    plt.plot(time, audio)

    for e in args[0]:
        plt.axvline(e / args[1], color='r', linestyle='--')

    plt.grid()
    plt.show()


def plot_signal_bubbles(audio: np.ndarray, begs: list, size: int, diameter: int):
    """Display a Bubble as a function of time.

    Args:
        audio (ndarray): Acoustic signal where the bubble is found.
        begs (list): Points where the bubbles begin.
        size (int): Size of the bubble.
        diameter (int): Diameter of the nozzle used in the title of the plot.
    """

    for _, beg in enumerate(begs):
        bubb, bubb_time = get_bubble(audio, beg, size)

        plt.title('Time Domain [Diameter of nozzle: {} mm]'.
                  format(diameter))
        plt.xlabel('Milissegundo')
        plt.ylabel('Amplitude')
        plt.plot(bubb_time, bubb)
        plt.xticks(np.arange(0, 100, 5))

    plt.grid()
    plt.show()


def plot_spectrogram(audio: np.ndarray, diameter: int, fs: int, *args):
    """Display the sprectrogram of the acoustic signal.

    Args:
        audio (np.ndarray): Acoustic signal to be plotted.
        diameter (int): Diameter of the nozzle used in the title of the plot.
        fs (int): The sampling frequency
        *args[ave (int)]: Average frequency of the acoustic signal.
    """

    plt.text(14, 9500, 'Mean Frequency: {} Hz'.format(int(args[0])), size=9,
             bbox=dict(boxstyle="round", edgecolor=(0.5, 0.5, 0.5), fill=False)
             )
    plt.title('Spectrogram [Diameter of nozzle: {} mm]'.format(diameter))
    plt.xlabel('Time [s]')
    plt.ylabel('Freq. [Hz]')
    plt.specgram(audio, Fs=fs, cmap='jet', NFFT=1024)
    plt.ylim(0, 10000)
    plt.yticks(np.arange(0, 10000, 1000))
    # plt.axhline(ave, color='r', alpha=0, label="Freq. Média: {} Hz".format(ave))

    cbar = plt.colorbar()
    cbar.set_label('rel to.')
    # cbar.set_ticks([])
    plt.show()


def videogram(audio: np.ndarray, audio_filt: np.ndarray, fs: int, fps: int = 30, btr: int = 3500):
    """Create an animated spectrogram along with the acoustic signal using the FFmpeg command.

    Args:
        audio (ndarray): Original acoustic signal.
        audio_filt (ndarray): Clean acoustic signal.
        fs (int): Sampling frequency.
        fps (int, optional): Number of frames per second to create the video. Defaults to 30.
        btr (int, optional): Bit rate to create the video. Defaults to 3500.
    """

    # Saving the audio file
    wavfile.write("cutted.wav", fs, audio)
    FFMpegWriter = animation.writers['ffmpeg']
    writer = FFMpegWriter(fps=fps, bitrate=btr, metadata=dict(
        title='Spectrogram Animation', artist='adejonghm', comment='LACMAM/POLI-USP'))

    duration = len(audio_filt) / fs
    freqs = np.fft.fftfreq(audio_filt.shape[0], 1/fs) / 1000
    max_freq_kHz = freqs.max()
    times = np.arange(audio_filt.shape[0]) / float(fs)

    fig = plt.figure(figsize=(10, 5))

    plt.subplot(2, 1, 1)
    plt.plot(times, (audio_filt).astype(float) /
             np.max(np.abs(audio_filt)), lw=0.1)

    plt.xlim(0, duration)
    plt.ylim(-1, 1)

    l1, = plt.plot([], [], color='k')

    plt.subplot(2, 1, 2)
    plt.specgram(audio_filt, Fs=fs, cmap=plt.get_cmap('jet'))
    plt.xlim(0, duration)
    plt.ylim(0, max_freq_kHz*500.0)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    formatter = FuncFormatter(lambda x, y: '%1.fk' % (x*1e-3))
    ax = plt.gca()
    ax.yaxis.set_major_formatter(formatter)

    l2, = plt.plot([], [], color='k')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.09, right=0.98,
                        top=0.98, left=0.08, hspace=0.14)

    x = np.array([0., 0.])
    y0 = np.array([-1, 1])
    y1 = np.array([0, max_freq_kHz*1000.0])

    # plt.savefig('spectrogram.jpg')

    with writer.saving(fig, "temp.mp4", 100):
        for _ in tqdm(range((int(duration)+1)*fps), desc="Creating video"):
            x += 1.0/float(fps)
            l1.set_data(x, y0)
            l2.set_data(x, y1)
            writer.grab_frame()

    os.system(
        "ffmpeg -y -i cutted.wav -i temp.mp4 -hide_banner -c:v copy -strict -2 specgram_animation.mp4")
    clear()
    os.system("rm temp.mp4")
    os.system("rm cutted.wav")


def create_signal(frequency: int, deltha: float, time: np.ndarray, amplitude: float = 1) -> np.ndarray:
    """Create an audio signal.

    Args:
        frequency (int): Frequency used to create the signal.
        deltha (float): The decay factor of the signal.
        time (np.ndarray): Time vector.
        amplitude (float, optional): Amplitude of the signal. Defaults to 1.

    Returns:
        np.ndarray: The acoustic signal.
    """

    omega = 2 * np.pi * frequency
    return amplitude * np.cos(omega * time) * np.exp(-np.pi * deltha * frequency * time)
