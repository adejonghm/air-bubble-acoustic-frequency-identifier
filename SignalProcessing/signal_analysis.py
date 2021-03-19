#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Used to carry out various analyses on the acoustic signal emitted by a controlled air bubble,
generated in the water. Sound Frequency Analysis is one of them.
"""


# Standard library imports
import argparse
import json
import os

# Third party imports
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal#, ndimage
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
from skimage import feature as sk_feature

# Local application imports
from dsip import sigproc as dsp
from dsip import improc as dip


# Setting Plot parameters
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['font.size'] = 8


if __name__ == "__main__":

    #### CONSTRUCT ARGUMENT PARSE
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True,
                    help="path to the input JSON file")
    args = vars(ap.parse_args())

    if args['file'].endswith('.json') and os.path.exists(args['file']):
        input_path = args['file']
    else:
        print('ERROR! JSON file not found.')
        os.sys.exit(1)

    #### READ JSON FILE
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    #### JSON PARAMETERS
    db_path = dataset[0]['path']
    size = dataset[0]['bubbleLength']

    #### JSON NODE
    node = dataset[2]
    diameter = node['diameter']
    beginnings = node['bubblesStart']
    node_path = db_path + node['path']
    audio_path = node_path + node['audioCutted']
    bw_img_path = node_path + node['bwFramesPath']

    #### LOADING AUDIO FILE
    Fs, wave = wavfile.read(audio_path)

    #### FILTERING THE SIGNAL
    sos = signal.butter(15, 500, 'hp', fs=Fs, output='sos')
    # sos = signal.butter(15, (500, 1500), 'bandpass', fs=Fs, output='sos')
    wave_filtered = signal.sosfilt(sos, wave)

    #### GETTING BW IMAGES LIST
    bw_images_list = sorted(os.listdir(bw_img_path))

    #### SETTING PARAMETERS
    Ts = 1 / Fs
    N = len(wave_filtered)
    time = np.arange(0, N/Fs, Ts)
    total_bubbles = len(beginnings)
    speed_deformation = []
    frequencies = []
    Eo, Re, k = 0, 0, 0
    _, index = bw_images_list[k].split('.')[0].split('-')

    #### CALCUTAING THE FFT OF A BUBBLE ####
    for i in range(1):
        bubb = dsp.get_bubble(wave_filtered, beginnings[i], size, Fs)

        fast_fourier_transform = abs(fft(2 * bubb[0]) / len(bubb[0]))
        position = fast_fourier_transform.tolist().index(max(fast_fourier_transform))
        f_axis = fftfreq(len(bubb[0])) * Fs
        freq = int(f_axis[position])
        radius = dsp.get_radius(freq)
        frequencies.append(freq)
        step = 5

        #### PLOTTING THE FFT OF A BUBBLE
        # plt.title('Frequency Domain [Diameter of nozzle: {} mm]'.format(diameter))
        # plt.xlabel('Freq. [Hz]')
        # plt.ylabel('F(t)')
        # plt.plot(f_axis, fast_fourier_transform)#, marker='.')
        # plt.xlim(0, 5000)

        #### ESTIMATING DEFORMATION RATE
        while int(index) - 1 == i:
            img_1 = dip.center_bubble(cv.imread(bw_img_path + bw_images_list[k], 0))
            _, img_1 = cv.threshold(img_1, 200, 255, cv.THRESH_BINARY)

            img_2 = dip.center_bubble(cv.imread(bw_img_path + bw_images_list[k+step], 0))
            _, img_2 = cv.threshold(img_2, 200, 255, cv.THRESH_BINARY)

            img_dif = abs(img_2 - img_1)

            ### Calculating Distance Transform
            dist_transform = cv.distanceTransform(img_dif.astype(np.uint8), cv.DIST_L2, 0)

            ### Coordinates Of Local Maxima
            coord_local_max = sk_feature.peak_local_max(dist_transform)

            ### Mean Of The Local Maxima
            local_max = np.array([dist_transform[x, y] for x, y in coord_local_max])
            mean_local_max = np.mean(local_max)

            ### Average Deformation Rate 
            speed_deformation = mean_local_max / (6e-2 * step)

            ### Getting The Next Image
            k += (step + 1)
            _, index = bw_images_list[k].split('.')[0].split('-')

        mean_speed_deformation = np.mean(speed_deformation)
        Eo = dsp.get_eotvos(radius)
        Re = dsp.get_reynolds(radius, mean_speed_deformation)

    #### WRITING MEAN FREQUENCY ON THE GRAPH ####
    # mean_freqs = np.mean(frequencies)
    # plt.text(1690, 110, 'Mean Frequency: {} Hz'.format(int(mean_freqs)), size=9,
    #          bbox=dict(boxstyle="round", edgecolor=(0.5, 0.5, 0.5), fill=False))
    # dsp.plot_signal_bubbles(wave_filtered, beginnings, size, diameter)

    # dsp.plot_spectrogram(wave_filtered, Fs, mean_freqs, diameter)

    # dsp.plot_signal(wave_filtered, diameter, time)#, Fs, beginnings)

    # dsp.videogram(wave, wave_filtered, Fs)

    ### CONSTRUCTING GRACE DIAGRAM ####
    print('Reynolds Numbers:', Re)
    print('Eötvös Numbers:', Eo)

    plt.title("Grace's Diagram")
    plt.xlabel('Eötvös Numbers (Eo)')
    plt.ylabel('Reynolds Numbers (Re)')
    plt.plot(Eo, Re, 'o', label='Nozzle {}mm'.format(diameter))
    plt.ticklabel_format(axis="y", style="plain", scilimits=(0, 0))
    plt.legend(loc='best')
    plt.show()
    