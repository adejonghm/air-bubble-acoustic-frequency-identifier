#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Used to carry out various analyses on the acoustic signal emitted by a controlled air bubble,
generated in the water. Sound Frequency Analysis is one of them.
"""


# Standard library imports
import json
import os
import sys

# Third party imports
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal#, ndimage
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
from skimage.feature import peak_local_max

# Local application imports
from dsip import sigproc as dsp
from dsip import improc as dip


# Setting Plot parameters
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['font.size'] = 8


if __name__ == "__main__":

    args = sys.argv

    if len(args) > 1:
        if args[1] == '-h':
            print('Syntax \n  python3 {} [OPTION] [FILE...]\n\n'
                  'OPTION \n  -f, --file\n'
                  '  Specify the path of the JSON file. You can use absolute or relative path.'.
                  format(args[0]))
            sys.exit(0)
        elif (args[1] == '-f' or args[1] == '--file') and len(args) == 3:
            if os.path.exists(args[2]) and args[2].endswith('.json'):
                input_path = args[2]
            else:
                print('ERROR! JSON file not found.')
                sys.exit(1)
        else:
            print('Syntax Error!!. Enter the [-h] option to display Help.')
            sys.exit(1)
    else:
        print('Syntax Error!!. Enter the [-h] option to display Help.')
        sys.exit(1)


    #### READ JSON FILE ####
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)


    #### JSON PARAMETERS ####
    db_path = dataset[0]['path']
    size = dataset[0]['bubbleLength']


    #### JSON NODE ####
    node = dataset[3]
    diameter = node['diameter']
    beginnings = node['bubblesStart']
    node_path = db_path + node['path']
    audio_path = node_path + node['audioCutted']
    bw_img_path = node_path + node['bwFramesPath']


    #### LOADING AUDIO FILE ####
    Fs, wave = wavfile.read(audio_path)


    #### FILTERING THE SIGNAL ####
    sos = signal.butter(15, 500, 'hp', fs=Fs, output='sos')
    wave_filtered = signal.sosfilt(sos, wave)


    #### GETTING BW IMAGES LIST ####
    bw_images = sorted(os.listdir(bw_img_path))
    total_images = len(bw_images)


    #### SETTING PARAMETERS ####
    Ts = 1 / Fs
    N = len(wave_filtered)
    # total_bubbles = len(beginnings)
    total_bubbles = 1
    frequencies = []
    speed_deformation = []
    Eo = []
    Re = []


    # Creating time vector (X axis)
    time = np.arange(0, N/Fs, Ts)


    #### CALCUTAING THE FFT OF A BUBBLE ####
    for i in range(total_bubbles):
        bubb = dsp.get_bubble(wave_filtered, beginnings[i], size, Fs)

        fast_fourier_transform = abs(fft(2 * bubb[0]) / len(bubb[0]))
        position = fast_fourier_transform.tolist().index(max(fast_fourier_transform))
        f_axis = fftfreq(len(bubb[0])) * Fs
        freq = int(f_axis[position])
        radius = dsp.get_radius(freq)
        frequencies.append(freq)
        step = 5


        #### PLOTTING THE FFT OF A BUBBLE ####
        # plt.title('Frequency Domain [Diameter of nozzle: {} mm]'.format(diameter))
        # plt.xlabel('Freq. [Hz]')
        # plt.ylabel('F(t)')
        # plt.plot(f_axis, fast_fourier_transform, marker='.')
        # plt.xlim(500, 2000)


        #### ESTIMATING DEFORMATION SPEED ####
        for k in range(0, total_images, step):
            img_1 = dip.center_bubble(cv.imread(bw_img_path + bw_images[0], 0))
            _, img_1 = cv.threshold(img_1, 200, 255, cv.THRESH_BINARY)

            img_2 = dip.center_bubble(cv.imread(bw_img_path + bw_images[4], 0))
            _, img_2 = cv.threshold(img_2, 200, 255, cv.THRESH_BINARY)

            img_dif = abs(img_2 - img_1)

            # Calculating distance transform
            dist_transform = cv.distanceTransform(img_dif.astype(np.uint8), cv.DIST_L2, 0)

            # coordinates of local maxima
            coord_local_max = peak_local_max(dist_transform)

            # mean of the local maxima
            local_max = np.array([dist_transform[x, y] for x, y in coord_local_max])
            mean_local_max = np.mean(local_max)

            # average deformation speed Comentar como se obtiene el valor (6e-2)
            speed_deformation.append(mean_local_max / (6e-2 * step))
            # speed_deformation = mean_local_max / (6e-2 * step)

            ### experimento para ver todas las desformaciones de la burbuja en el recorrido
            # Re.append(dsp.get_reynolds(radius, speed_deformation))
            # speed_deformation = mean_local_max / (6e-2 * step)

        mean_speed_deformation = np.mean(speed_deformation)
        Eo.append(dsp.get_eotvos(radius))
        Re.append(dsp.get_reynolds(radius, mean_speed_deformation))

    #### experimento para mostrar cada par de imagenes
    # np.savetxt('Numeros de Reynolds.csv', Re, fmt='%0.15f')
    # print(Re)

    #### WRITING MEAN FREQUENCY ON THE GRAPH ####
    # mean_freqs = np.mean(frequencies)
    # plt.text(1690, 110, 'Mean Frequency: {} Hz'.format(int(mean_freqs)), size=9,
    #          bbox=dict(boxstyle="round", edgecolor=(0.5, 0.5, 0.5), fill=False)
    #          )
    # dsp.plot_signal_bubbles(wave_filtered, beginnings, size, diameter)

    # dsp.plot_spectrogram(wave_filtered, diameter, Fs, mean_freqs)

    dsp.plot_signal(wave_filtered, diameter, time)#, Fs, beginnings)

    # dsp.videogram(wave, wave_filtered, Fs)


    #### CONSTRUCTING GRACE DIAGRAM ####
    # print("")
    # print(f'Media De Todas Velocidades De Deformacion: {round(mean_speed_deformation, 3)}')
    # print(f'Radio: {round(radius * 1000, 3)}')
    # print(f'Re: {round(Re[0], 3)}')

    plt.title("Grace's Diagram")
    plt.xlabel('Eötvös Numbers (Eo)')
    plt.ylabel('Reynolds Numbers (Re)')
    plt.plot(Eo, Re, 'o', label='Nozzle {}mm'.format(diameter))
    plt.ticklabel_format(axis="y", style="plain", scilimits=(0, 0))
    plt.legend(loc='best')
    plt.show()



    ################################################################


    # print('La suma es:', np.sum(local_max))
    # print('La media es:', mean)
    # print('El maximo local es:', np.amax(local_max))
    # print('La velocidad de deformacion es:', speed_deformation)

    # x_T = 180
    # x_B = 145

    # y_T = 175
    # y_B = 140
    # plt.subplot(221)
    # plt.imshow(img_1[y_B:y_T, x_B:x_T])
    # plt.title(f'Image {bw_images[0]}')
    # plt.axis(False)

    # plt.subplot(222)
    # plt.imshow(img_2[y_B:y_T, x_B:x_T])
    # plt.title(f'Image {bw_images[4]}')
    # plt.axis(False)

    # plt.subplot(223)
    # plt.imshow(dist_transform[y_B:y_T, x_B:x_T])
    # plt.title('Transforamda Distancia')
    # plt.axis(False)

    # plt.subplot(224)
    # plt.imshow(np.zeros_like(img_dif))
    # plt.plot(coord_local_max[:, 1], coord_local_max[:, 0], '.', color='w')
    # plt.xlim(x_B, x_T)
    # plt.ylim(y_T, y_B)
    # plt.title('Maximos Locais')
    # plt.axis(False)

    # plt.show()
    