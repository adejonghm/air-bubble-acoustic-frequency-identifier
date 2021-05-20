#!/usr/bin/env python3

"""
Created on:	 April, 2020
@uthor: 	 adejonghm
----------

"""

# Standard library imports
import argparse
import json
import os

# Third party imports
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
# from tqdm import tqdm

# Local application imports
from dsip import improc as dip
from dsip.drlse import drlse_edge


if __name__ == "__main__":

    ## CONSTRUCT ARGUMENT PARSE ##
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

    ## READ JSON FILE ##
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    ## LOADING JSON DATA ##
    # general data
    db_path = dataset[0]['path']
    backg_path = db_path + 'background.jpg'
    backg = cv.imread(backg_path, 0)

    # node data
    node = dataset[3]
    node_path = db_path + node['path']
    diameter = node['diameter']
    area_coord = node['flowAreaCoord']
    bw_frames_path = node_path + node['bwFramesPath']
    frames_path = node_path + node['framesPath']
    frames = sorted(os.listdir(frames_path))
    total_frames = len(frames)

    ## SETTING PARAMETERS ##
    # Time step, reasonable values in range [0.1; 5].
    timestep = 2

    # Coefficient of the distance regularization term R(phi),
    # Must respect the CFL condition (mu_max = 0.25/timestep).
    mu = 0.2/timestep

    # Coefficient of the weighted length term L(phi).
    lmda = 10

    # Scale parameter in Gaussian kernel
    # Reasonable values in range [0.7; 2] pixels.
    sigma = 0.7

    # Positive parameter that specifies the width of the DiracDelta function in pixels.
    # Smaller values lead to a zero level contour with lots of details, whereas larger
    # ones lead to a smooth zero level contour.
    epsilon = 2.0

    # Coefficient of the weighted area term A(phi).
    # Positive values make level set contour shrink and negative values lead it to expand.
    # The magnitude influences speed of shrinkage/expansion.
    alpha = 2

    # Initial values for binary LSF. Should be positive.
    # Reasonable values in range [2 10]. Too small values may lead to identifying
    # small contours (or no zero level contour). Small values in range tend
    # to provide faster motion for zero level contour. Too large values lead to a stiff
    # level set function, i.e., to a zero level contour that does not change much.
    c = 2

    # Number of iterations in internal loop
    iter_inner = 20

    # Number of iterations in external loop
    iter_outer = 30
    potential = 2
    if potential == 1:
        potential_function = 'single-well'
    else:
        potential_function = 'double-well'

    # Selector to decide which bubble is taken
    flowing = True

    ## Indicate if the object is selected
    selected = 1

    ## START PROCESSING ##
    for i in range(total_frames):

        ## LOADING IMAGE ##
        full_name_frame = frames[i]
        short_name_frame, _ = full_name_frame.split('.')
        frame = cv.imread(frames_path + full_name_frame, 0)

        ## REMOVIMG BACKGROUND ##
        img = dip.subtract(frame, backg, thresh=15)
        if diameter == 4:
            img = img[5:195, ...]
        else:
            img = img[5:220, ...]

        ## SMOOTHING IMAGE BY GAUSSIAN CONVOLUTION ##
        smoothed_img = dip.clean_image(img, area_coord, sigma)

        if np.count_nonzero(smoothed_img):
            ## CALCULATE GRADIENT & DEFINE EDGE INDICATOR FUNCTION ##
            [Iy, Ix] = np.gradient(smoothed_img)
            f = np.square(Ix) + np.square(Iy)
            edge_indicator_function = 1 / (1 + f)

            ## INITIALIZE LSF AS BINARY STEP FUNCTION & GENERATE THE INITIAL REGION R0 ##
            init_LSF = c * np.ones(smoothed_img.shape)
            init_LSF[1:-5, 140:215] = -c
            phi = init_LSF.copy()

            ## START LEVEL SET EVOLUTION ##
            for k in range(iter_outer):
                phi = drlse_edge(phi, edge_indicator_function, lmda, mu,
                                 epsilon, timestep, iter_inner, potential_function, alpha)
                # if np.mod(k, 2) == 0:
                #     plt.clf()
                #     dip.get_image_contours(img, phi, fig_title=short_name_frame)
                #     plt.pause(0.1)

            ## REFINE THE ZERO LEVEL CONTOUR BY FURTHER LEVEL SET EVOLUTION WITH (alpha=0) ##
            # Number of iterations in internal loop made at the end, with α=0.
            iter_refine = 10
            phi = drlse_edge(phi, edge_indicator_function, lmda, mu,
                             epsilon, timestep, iter_refine, potential_function)

            ## BINARIZE IMAGE ##
            final_LSF = np.array(phi.copy())
            (_, bw_image) = cv.threshold(final_LSF, 0, 255, cv.THRESH_BINARY_INV)

            ## DETECTING BUBBLE ##
            (selected, flowing, bw_image) = dip.get_main_bubble(
                bw_image, flowing, selected)

            if flowing:
                ## SAVE IMAGE WITH DRLSE ##
                dip.get_image_contours(smoothed_img, final_LSF)
                plt.axis(False)
                plt.close()

                ## SAVE BINARY IMAGE ##
                cv.imwrite('{}{}-{}.jpg'.
                           format(bw_frames_path, short_name_frame, selected), bw_image)

                ## SHOW MESSAGE ##
                print('Image {} for nozzle diameter {} mm was segmented.'.
                      format(short_name_frame, diameter))
        else:
            pass
    # ## ENDFOR ##
