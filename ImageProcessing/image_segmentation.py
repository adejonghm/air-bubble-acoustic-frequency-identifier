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
from dsip.gfd import generic_fourier_descriptor


if __name__ == "__main__":

    #### CONSTRUCT ARGUMENT PARSE ####
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True,
                    help="path to the input JSON file")
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
    node = dataset[3]
    node_path = db_path + node['path']
    diameter = node['diameter']
    area_coord = node['flowAreaCoord']
    segmented_frames_path = node_path + node['segmentedFramesPath']
    bw_frames_path = node_path + node['bwFramesPath']
    frames_path = node_path + node['framesPath']
    frames = sorted(os.listdir(frames_path))
    total_frames = len(frames)

    #### SETTING PARAMETERS ####
    ## Time step, reasonable values in range [0.1; 5].
    timestep = 2

    ## Coefficient of the distance regularization term R(phi),
    ## Must respect the CFL condition (mu_max = 0.25/timestep).
    mu = 0.2/timestep

    ## Coefficient of the weighted length term L(phi).
    lmda = 10

    ## Scale parameter in Gaussian kernel
    ## Reasonable values in range [0.7; 2] pixels.
    sigma = 0.7

    ## Positive parameter that specifies the width of the DiracDelta function in pixels.
    ## Smaller values lead to a zero level contour with lots of details, whereas larger
    ## ones lead to a smooth zero level contour.
    epsilon = 2.0

    ## Coefficient of the weighted area term A(phi).
    ## Positive values make level set contour shrink and negative values lead it to expand.
    ## The magnitude influences speed of shrinkage/expansion.
    alpha = 2

    ## Initial values for binary LSF. Should be positive.
    ## Reasonable values in range [2 10]. Too small values may lead to identifying
    ## small contours (or no zero level contour). Small values in range tend
    ## to provide faster motion for zero level contour. Too large values lead to a stiff
    ## level set function, i.e., to a zero level contour that does not change much.
    c = 2

    ## Number of iterations in internal loop
    iter_inner = 20

    ## Number of iterations in external loop
    iter_outer = 30
    potential = 2
    if potential == 1:
        potential_function = 'single-well'
    else:
        potential_function = 'double-well'

    ## Selector to decide which bubble is taken
    flowing = False

    ##
    selected = 0

    #### START PROCESSING ####
    for i in range(total_frames): #1644, 1646

        #### LOADING IMAGE ####
        full_name_frame = frames[i]
        short_name_frame = full_name_frame.split('.')[0]
        frame = cv.imread(frames_path + full_name_frame, 0)

        #### REMOVIMG BACKGROUND ####
        img = dip.subtract(frame, backg, thresh=15)
        if diameter == 4:
            img = img[5:195, ...]
        else:
            img = img[5:220, ...]

        #### SMOOTHING IMAGE BY GAUSSIAN CONVOLUTION ####
        smoothed_img = dip.clean_image(img, area_coord, sigma)

        if np.count_nonzero(smoothed_img):
            #### CALCULATE GRADIENT & DEFINE EDGE INDICATOR FUNCTION ####
            [Iy, Ix] = np.gradient(smoothed_img)
            f = np.square(Ix) + np.square(Iy)
            edge_indicator_function = 1 / (1 + f)

            #### INITIALIZE LSF AS BINARY STEP FUNCTION & GENERATE THE INITIAL REGION R0
            init_LSF = c * np.ones(smoothed_img.shape)
            init_LSF[1:-5, 140:215] = -c
            phi = init_LSF.copy()

            ### START LEVEL SET EVOLUTION ####
            for k in range(iter_outer):
                phi = drlse_edge(phi, edge_indicator_function, lmda, mu,
                                 epsilon, timestep, iter_inner, potential_function, alpha)
                # if np.mod(k, 2) == 0:
                #     plt.clf()
                #     dip.get_image_contours(smoothed_img, phi, fig_title=short_name_frame)
                #     plt.pause(0.1)

            #### REFINE THE ZERO LEVEL CONTOUR BY FURTHER LEVEL SET EVOLUTION WITH (alpha=0) ####
            ## Number of iterations in internal loop made at the end, with α=0.
            iter_refine = 10
            phi = drlse_edge(phi, edge_indicator_function, lmda, mu,
                             epsilon, timestep, iter_refine, potential_function)

            #### BINARIZE IMAGE ####
            final_LSF = np.array(phi.copy())
            (_, bw_image) = cv.threshold(final_LSF, 0, 255, cv.THRESH_BINARY_INV)

            #### DETECTING BUBBLE ####
            flowing, bw_image = dip.get_main_bubble(bw_image, area_coord, sigma, flowing)

            if not flowing:
                selected += 1

            #### SAVE IMAGE WITH DRLSE ####
            dip.get_image_contours(smoothed_img, final_LSF)
            plt.axis(False)
            plt.savefig('{}{}'.format(segmented_frames_path, full_name_frame),
                        bbox_inches='tight', pad_inches=0)#, dpi=65.5)
            plt.close()

            #### SAVE BINARY IMAGE ####
            cv.imwrite("{}{}".format(bw_frames_path, full_name_frame), bw_image)
            # # plt.imsave("{}{}".format(bw_frames_path, full_name_frame), bw_image)

            #### FOURIER DESCRIPTORS & CENTROID ####
            square_image = dip.center_bubble(bw_image)
            fd_bubble = generic_fourier_descriptor(square_image, 1, 10)
            cX, cY = dip.get_centroid(bw_image)

            # plt.figure(figsize=(7, 4))
            # plt.title('Desc. de Fourier da imagen {}, vocal {}mm'.
            #           format(short_name_frame, diameter))
            # plt.yticks(np.arange(0, 1, 0.05))
            # plt.xticks(np.arange(0, 14, 1))
            # plt.stem(fd_bubble, use_line_collection=True)
            # plt.show(block=False)
            # plt.pause(1)
            # plt.close()

            #### VOLUME CALCULATION ####
            volume = dip.get_bubble_volume(bw_image, 0.3846)

            #### SHOW MESSAGE ####
            print(f'Diameter {diameter}mm, Image {short_name_frame}', selected)
            # print("")
            # print("|-----------------| RESULT OF IMG {} |-------------------|".
            #       format(short_name_frame))
            # print('| Diameter of the nozzle: {} mm\t\t\t\t    |'.format(diameter))
            # print('| Image volume is: {} mm^3\t\t\t\t    |'.
            #       format(round(volume, 2)))
            # print('| Image segmented and successfully saved as binary.\t    |')
            # print('| Centroid coordinates are: ({}, {})\t\t    |'.
            #       format(round(cX, 1), round(cY, 1)))
            # print('| The sum of FD is: {} and the total of FD is: {} |'.
            #       format(sum(fd_bubble), len(fd_bubble)))
            # print('|-----------------------------------------------------------|')
        else:
            pass

    # ####### ENDFOR #########
