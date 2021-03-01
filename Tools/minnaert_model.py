#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

MATHEMATICAL MODEL PROPOSED BY MINNAERT IN 1933 TO CALCULATE
THE NATURAL FREQUENCY OF THE ACOUSTIC EMISSION OF A BUBBLE
"""

# Standard library imports
from math import pi


specific_heat_ratio = 1.40      # Specific Heat Radio. (k = Cp/Cv)
# radio = 0.0033                  # Initial radius of the bubble. Expressed in meters [m]
freq = 724                      # Natural frequency of the bubble captured with a hydrophone, [Hz]
rho = 998                       # Liquid Water Density (rho). Expressed in [Kg/m^3]
atm_pressure = 101325           # Atmospheric pressure taking it as initial pressure . [Pa]

# freq = ((3 * specific_heat_ratio * atm_pressure / rho) ** (1/2)) / (2 * pi * radio)
radio = ((3 * specific_heat_ratio * atm_pressure / rho) ** (1/2)) / (2 * pi * freq)

print("radius: {:.2f}[mm], Frequency: {:.0f}[Hz]".format(radio*1000, freq))
