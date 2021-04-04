#!/usr/bin/env python3
# type: ignore

"""
Dev: 	adejonghm
----------

Calculate the mean and variance of the radii for each scenario.
"""

# Standard library imports
import argparse
import json
import os

# Third party imports
import numpy as np


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

    ## READ JSON FILE
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    ## JSON NODE
    db_path = dataset[0]['path']
    node = dataset[2]
    diameter = node['diameter']
    node_path = db_path + node['path'] + 'volumes_radii.json'

    ## LOAD BUBBLES RADII
    with open(node_path, 'r', encoding='utf-8') as file:
        radii_file = json.load(file)

    ## CALCULATE VARIANZE AND MEAN
    radii = np.array(radii_file['radii_from_images'])
    mean = np.mean(radii)
    variance = np.var(radii)
    print('Nozzle:', diameter, "mm")
    print('Mean:', round(mean, 3))
    print('Variance:', round(variance, 3))
