#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

This is a version of generic Fourier Descriptors (GFD) implemented in Python based on the article:
D. Zhang & G. Lu, Shape based image retrieval using generic Fourier Descriptors, 2002
"""

# Standard library imports
from math import sqrt, pi

# Third party imports
import numpy as np

# Local application imports


def generic_fourier_descriptor(bw, m, n):
    """[summary]

    Args:
        bw ([type]): [description]
        m ([type]): [description]
        n ([type]): [description]

    Returns:
        [type]: [description]
    """
    if len(bw.shape) > 2:
        bw = bw.max(axis=2) / 255

    N = bw.shape[1]

    # GET THE MAXIMAL RADIUS MAXR
    maxRad = sqrt((N // 2)**2 + (N // 2)**2)
    # Determinar el maximo de maxRad

    # MESHGRID WITH ORIGIN CENTERED TO THE IMAGE CENTER
    x = np.linspace(-(N-1) // 2, (N-1) // 2, N)
    y = x
    X, Y = np.meshgrid(x, y)

    # MATRIX CONTAINING RADIUS OF EACH CELL TO IMAGE CENTER
    radius = np.sqrt(np.power(X, 2) + np.power(Y, 2)) / maxRad

    # MATRIX CONTAINING ANGLUAR OF EACH CELL TO IMAGE CENTER
    theta = np.arctan2(Y, X)
    theta[theta < 0] = theta[theta < 0] + 2 + pi

    # INITIALIZE VARIABLES
    FR = np.zeros((m, n))
    FI = np.zeros((m, n))
    FD = np.zeros((m*n, 1))

    i = 0
    # LOOP OVER ALL RADIAL FREQUENCIES
    for rad in range(m):

        # LOOP OVER ALL ANGULAR FREQUENCIES
        for ang in range(n):

            # CALCULATE FR AND FI FOR (RAD,ANG)
            tempR = bw * np.cos(2*pi * rad * radius + ang * theta)
            tempI = -bw * np.sin(2*pi * rad * radius + ang * theta)
            FR[rad, ang] = np.sum(tempR)
            FI[rad, ang] = np.sum(tempI)

            # CALCULATE FD, WHERE FD(END)=FD(0,0) --> RAD == 0 & ANG == 0
            if rad == 0 and ang == 0:
                # NORMALIZED BY CIRCLE AREA
                FD[i] = sqrt(FR[0, 0]**2 + FR[0, 0]**2) / (pi * maxRad**2)
            else:
                # NORMALIZED BY |FD(0,0)|
                FD[i] = sqrt(FR[rad, ang]**2 + FI[rad, ang]**2) / sqrt(FR[0, 0]**2 + FR[0, 0]**2)
            i += 1
    return FD
