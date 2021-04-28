#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

MATHEMATICAL MODEL PROPOSED BY MINNAERT IN 1933 TO CALCULATE
THE NATURAL FREQUENCY OF THE ACOUSTIC EMISSION OF A BUBBLE
"""

# Standard library imports
from math import pi
import json


if __name__ == '__main__':
    with open('frequencies.json', encoding='utf-8') as f:
        dataset = json.load(f)

    # Natural frequency of the bubble captured with a hydrophone, [Hz]
    frequencies = dataset[2]['frequencies']

    # Specific Heat Radio. (k = Cp/Cv)
    specific_heat_ratio = 1.40

    # Initial radius of the bubble. Expressed in meters [m]
    # radio = 0.0033

    # Liquid Water Density (rho). Expressed in [Kg/m^3]
    rho = 998

    # Atmospheric pressure taking it as initial pressure . [Pa]
    atm_pressure = 101325

    # freq = ((3 * specific_heat_ratio * atm_pressure / rho) ** (1/2)) / (2 * pi * radio)
    # radio = ((3 * specific_heat_ratio * atm_pressure / rho) ** (1/2)) / (2 * pi * freq)

    radii = []
    for f in frequencies:
        radio = ((3 * specific_heat_ratio * atm_pressure / rho) ** (1/2)) / (2 * pi * f)
        radii.append(round(radio * 1000, 2))
        print("radius: {:.02f}[mm], Frequency: {}[Hz]".format(radio*1000, f))
