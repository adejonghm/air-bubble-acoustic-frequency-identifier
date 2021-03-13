#!/usr/bin/env python3

"""
Created on:	 May, 2020
@uthor: 	 adejonghm
----------

This module was implemented in order to create functions used in
the image processing performed.
"""


import cv2 as cv
import numpy as np

from math import pi
from typing import TypeVar
from skimage import measure
from matplotlib import pyplot as plt


# Setting types
ndarray = TypeVar("np.ndarray")

# Setting Color Map
plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['figure.dpi'] = 100.0
plt.rcParams['figure.figsize'] = (4.14, 2.97)


def get_image_contours(image: ndarray, ctr_param: ndarray, fig_title: str = None):
    """Display the contours of an object over an image.

    Args:
        image (ndarray): Image like 2-D array for grayscale or 3-D array for RGB image.
        ctr_param (ndarray): Function used to calculate and show the contours.
        fig_title (str, optional): Title of the figure. Defaults to None.
    """

    plt.title(fig_title)
    plt.imshow(image)
    contours = measure.find_contours(ctr_param, 0)
    for contour in contours:
        plt.plot(contour[:, 1], contour[:, 0], color='r', linewidth=1.5)


def get_centroid(image: ndarray) -> tuple:
    """Determine the X and Y coordinates of the Centroid on the
    object that appears in the image.

    Args:
        image (ndarray): Image with one chanel.

    Returns:
        tuple: Coordinates (x, y) of the Centroid on the object.
    """

    M = cv.moments(image)

    cX = M['m10'] / M['m00']
    cY = M['m01'] / M['m00']

    return (cX, cY)


def get_main_bubble(image: ndarray, flag: bool, iteration: int) -> ndarray:
    """Select the main bubble in the image based on its size.

    Args:
        image (ndarray): Grayscale Image with one channel.
        flag (bool): Selector to decide which bubble is taken.
        iteration (int): The number of the bubble used to rename the binary image.

    Returns:
        ndarray: A new image with the main object.
    """

    contours = measure.find_contours(image, 0)
    print(len(contours))
    lengths = [len(item) for i, item in enumerate(contours)]
    index = lengths.index(max(lengths))

    # GET THE OBJECT
    bub = contours[index].astype(int)
    y_min, y_max = min(bub[:, 0]), max(bub[:, 0])
    x_min, x_max = min(bub[:, 1]), max(bub[:, 1])

    # RELEASING THE FLAG WHEN THE BUBBLE REACHES THE TOP
    lengths = [len(item) for i, item in enumerate(contours)]
    print(lengths)
    y_min, y_max = min(contours[0][:, 0]), max(contours[0][:, 0])
    if flag and y_min < 8:
        flag = False

    # INCREASING THE NUMBER OF THE BUBBLE WHEN IT STARTS AGAIN
    if not flag and y_max >= 190:
        iteration += 1
        flag = True

    # CREATE THE NEW IMAGE WITH THE OBJECT
    new_image = np.zeros_like(image)
    new_image[y_min:y_max, x_min:x_max] = image[y_min:y_max, x_min:x_max]

    return (iteration, flag, new_image)


def get_number_of_bubble(image: ndarray) -> int:
    """Get the number of bubbles in a image

    Args:
        image (ndarray): Grayscale input image with a single channel.

    Returns:
        int: Number of bubble in the image.
    """

    contours = measure.find_contours(image, 0)
    return len(contours)


def get_bubble_volume(image: ndarray, scale_factor: float) -> float:
    """Calculate the volume of the bubble that appears in the image.
    The volume is calculated in each row of the image, using the
    scale_factor parameter as the height in the equation.

    Args:
        image (ndarray): Image as Numpy Array with one chanel.
        scale_factor (float): Convection value of 1 pixel in millimeters.

    Returns:
        float: Volume of the bubble.
    """

    volume = 0
    for px in range(image.shape[0]):
        if 255 in image[px]:
            radius = (np.count_nonzero(image[px] == 255) / 2) * scale_factor
            volume += pi * (radius ** 2) * scale_factor

    return volume


def clean_image(image: ndarray, coord: list, sigmaX: float) -> ndarray:
    """Select the flow area in the image, with the objects.

    Args:
        image (ndarray): Grayscale Image with one channel.
        coord (list): Coordinates of the selected area.
        sigmaX (float): Gaussian kernel standard deviation.

    Returns:
        ndarray: A new image with the flow area.
    """

    # APPLY GUASSIAN BLUR
    smoothed_image = cv.GaussianBlur(image, (5, 5), sigmaX)

    # FIND CONTOURS
    contours = measure.find_contours(smoothed_image, 0)
    lengths = [len(item) for i, item in enumerate(contours)]

    # CREATE NEW IMAGE WITH MAIN BUBBLE
    new_image = np.zeros_like(image)

    # GET DELIMITERS FROM THE FLOW AREA
    y_min, y_max, x_min, x_max = coord[0], coord[1], coord[2], coord[3]

    if any(i >= 70 for i in lengths):
        new_image[y_min:y_max, x_min:x_max] = image[y_min:y_max, x_min:x_max]
        return cv.GaussianBlur(new_image, (5, 5), sigmaX)
    else:
        return np.zeros_like(image)


def detect_bubble(image: ndarray) -> int:
    """Determine the number of object on the image.

    Args:
        image (ndarray): Image with one chanel.

    Returns:
        int: Number of object on the image.
    """

    number_of_obj = len(measure.find_contours(image, 0))
    if number_of_obj == 0:
        return 0
    else:
        return number_of_obj


def center_bubble(image: ndarray) -> ndarray:
    """Center the object on the image. The image can only have
    a single object. In case the original image is not square,
    the new image will be square with the object in the center.

    Args:
        image (ndarray): Image with one chanel.

    Returns:
        ndarray: Image with the object in the center.
    """

    image = image.astype('uint8')
    height, width = image.shape

    if height == width:
        # RECENTER
        x, y, w, h = cv.boundingRect(image)

        offsetX = (width - w)//2
        offsetY = (height - h)//2

        square_fig = np.zeros_like(image)
        square_fig[offsetY:offsetY+h, offsetX:offsetX+w] = image[y:y+h, x:x+w]

        return square_fig

    else:
        # CREATING SQUARE IMAGE
        dim = image.shape
        imax = np.max(dim)
        imin = np.min(dim)
        max_pos = np.argmax(dim)

        new_dim = np.zeros(2, np.int_)
        for i in range(2):
            if i == max_pos:
                new_dim[i] = imax
            else:
                new_dim[i] = imax-imin

        comp = np.zeros(new_dim)
        if max_pos == 0:
            square_fig = np.concatenate((image, comp), axis=1)
        else:
            square_fig = np.concatenate((image, comp), axis=0)

        # RECENTER
        x, y, w, h = cv.boundingRect(image)
        offsetX = (square_fig.shape[1] - w)//2
        offsetY = (square_fig.shape[0] - h)//2
        square_fig = np.zeros_like(square_fig)
        square_fig[offsetY:offsetY+h, offsetX:offsetX+w] = image[y:y+h, x:x+w]

        return square_fig


def subtract(image1: ndarray, image2: ndarray, thresh: int) -> ndarray:
    """Subtract (image1 - image2) pixel by pixel that has the same
    dimensions, putting zero where the result is less than 20.

    Args:
        image1 (ndarray): Image to be subtract.
        image2 (ndarray): Image to be subtract.
        thresh (int): Value used as a threshold in subtraction to put zero on the result.

    Returns:
        ndarray: Image with zeros in negative values.
    """

    row_len, col_len = image1.shape
    result = np.zeros_like(image1, np.uint8)

    for row in range(row_len):
        for col in range(col_len):
            num = float(image1[row, col]) - float(image2[row, col])

            if num < thresh:
                result[row, col] = 0
            else:
                result[row, col] = num

    return result
