#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------


"""

# Standard library imports
import argparse
import json
import os
from math import pi

# Third party imports
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
# from tqdm import tqdm

# Local application imports
from dsip import improc as dip
from dsip.gfd import generic_fourier_descriptor


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

    #### LOADING JSON DATA ####
    # general data
    db_path = dataset[0]['path']
    backg_path = db_path + 'background.jpg'
    backg = cv.imread(backg_path, 0)

    # node data
    node = dataset[2]
    node_path = db_path + node['path']
    diameter = node['diameter']
    bw_frames_path = node_path + node['bwFramesPath']
    frames = sorted(os.listdir(bw_frames_path))
    total_frames = [1]
    volumes = []
    radii = []


    for i in total_frames:

        #### LOADING IMAGE ####
        full_name_frame = frames[i-1]
        short_name_frame = full_name_frame.split('.')[0].split('-')[1]

        frame = cv.imread(bw_frames_path + full_name_frame, 0)
        _, bw_image = cv.threshold(frame, 200, 255, cv.THRESH_BINARY)

        #### FOURIER DESCRIPTORS & CENTROID ####
        square_image = dip.center_bubble(bw_image)
        fd_bubble = generic_fourier_descriptor(square_image, 1, 10)
        cX, cY = dip.get_centroid(bw_image)

        fig, (a, b) = plt.subplots(1, 2)
        fig.set_size_inches(13, 4)
        fig.suptitle(f'Desc. de Fourier da imagen {short_name_frame}, bico {diameter}mm',
                     fontsize=15)

        # a.imshow(bw_image)
        # a.axis(False)

        # b.set_yticks(np.arange(0, 1, 0.05))
        # b.set_xticks(np.arange(0, 14, 1))
        # b.stem(fd_bubble, use_line_collection=True)

        # # plt.show()
        # plt.show(block=False)
        # plt.pause(2)
        # plt.close()

        #### VOLUME CALCULATION ####
        vol = dip.get_bubble_volume(bw_image, 0.3846)
        radius = pow((3 * vol) / (4 * pi), 1/3)

        radii.append(round(radius, 2))
        volumes.append(round(vol, 2))

        # print(
        #     f'|-----------------| RESULT OF IMG {short_name_frame} |------------------|')
        # print(f' Image volume is: {vol} mm^3')
        # print(f' Centroid coordinates are: ({round(cX, 1)}, {round(cY, 1)})')
        # print(f' The sum of FD is: {sum(fd_bubble)} and the total of FD is: {len(fd_bubble)}')
        # print('|----------------------------------------------------------|')

    print('volume:', volumes)
    print('radius:', radii)
