#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

This Matlab code implements an edge-based active contour model as
an application of the Distance Regularized Level Set Evolution (DRLSE)
formulation in Li et al's paper: 

C. Li, C. Xu, C. Gui, M. D. Fox, IEEE Trans. Image Processing, vol. 19 (12), pp.3243-3254, 2010.
"""

# Standard library imports

# Third party imports
import numpy as np
import scipy.ndimage.filters as filters


def div(nx, ny):
    """
    Args:
        nx ([type]): [description]
        ny ([type]): [description]

    Returns:
        [type]: [description]
    """

    [_, nxx] = np.gradient(nx)
    [nyy, _] = np.gradient(ny)

    return nxx + nyy


def distReg_p2(phi):
    """
    Compute the distance regularization term with the double-well
    potential p2 in equation (16)
    """

    [phi_y, phi_x] = np.gradient(phi)
    s = np.sqrt(np.square(phi_x) + np.square(phi_y))
    a = (s >= 0) & (s <= 1)
    b = (s > 1)

    # compute first order derivative of the double-well potential p2 in equation (16)
    ps = a * np.sin(2 * np.pi * s) / (2 * np.pi) + b * (s - 1)

    # compute d_p(s)=p'(s)/s in equation (10).
    # As s-->0, we have d_p(s)-->1 according to equation (18)
    dps = ((ps != 0) * ps + (ps == 0)) / ((s != 0) * s + (s == 0))

    return div(dps * phi_x - phi_x, dps * phi_y - phi_y) + filters.laplace(phi, mode='wrap')


def dirac(x, sigma):
    """
    Args:
        x ([type]): [description]
        sigma ([type]): [description]

    Returns:
        [type]: [description]
    """

    f = (1 / 2 / sigma) * (1 + np.cos(np.pi * x / sigma))
    b = (x <= sigma) & (x >= -sigma)

    return f * b


def neumannBound(f):
    """ Make a function satisfy Neumann boundary condition """

    [ny, nx] = f.shape
    g = f.copy()

    g[0, 0] = g[2, 2]
    g[0, nx-1] = g[2, nx-3]
    g[ny-1, 0] = g[ny-3, 2]
    g[ny-1, nx-1] = g[ny-3, nx-3]

    g[0, 1:-1] = g[2, 1:-1]
    g[ny-1, 1:-1] = g[ny-3, 1:-1]

    g[1:-1, 0] = g[1:-1, 2]
    g[1:-1, nx-1] = g[1:-1, nx-3]

    return g


def drlse_edge(phi_0, g, lmda, mu, epsilon, timestep, iters, potentialFunction, alpha=0):
    """Updated Level Set Function

    Args:
        phi_0: level set function to be updated by level set evolution.
        g: edge indicator function.
        lmda: weight of the weighted length term.
        mu: weight of distance regularization term.
        epsilon: width of Dirac Delta function.
        timestep: time step.
        iters: number of iterations.
        potentialFunction: choice of potential function in distance regularization term.
                            As mentioned in the above paper, two choices are provided:
                            potentialFunction='single-well' or potentialFunction='double-well',
                            which correspond to the potential functions p1 (single-well) and
                            p2 (double-well), respectively.
        alpha (int, optional): weight of the weighted area term. Defaults to 0.
    """

    phi = phi_0.copy()
    [vy, vx] = np.gradient(g)

    i = 0
    while i < iters:
        phi = neumannBound(phi)
        [phi_y, phi_x] = np.gradient(phi)
        s = np.sqrt(np.square(phi_x) + np.square(phi_y))
        smallNumber = 1e-10
        # add a small positive number to avoid division by zero
        Nx = phi_x / (s + smallNumber)
        Ny = phi_y / (s + smallNumber)
        curvature = div(Nx, Ny)
        if potentialFunction == 'single-well':
            # compute distance regularization term
            # in equation (13) with the single-well potential p1.
            distRegTerm = filters.laplace(phi, mode='wrap') - curvature
        elif potentialFunction == 'double-well':
            # compute the distance regularization term
            # in eqaution (13) with the double-well potential p2.
            distRegTerm = distReg_p2(phi)
        else:
            print('Error: Wrong choice of potential function. Please input the'
                  'string "single-well" or "double-well" in the drlse_edge function.')
        diracPhi = dirac(phi, epsilon)
        areaTerm = diracPhi * g  # balloon/pressure force
        edgeTerm = diracPhi * (vx * Nx + vy * Ny) + diracPhi * g * curvature
        phi = phi + timestep * (mu * distRegTerm + lmda * edgeTerm + alpha * areaTerm)

        i += 1

    return phi
