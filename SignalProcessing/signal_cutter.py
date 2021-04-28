#!/usr/bin/env python3

"""
Dev: 	adejonghm
----------

Used to cut the precise time interval obtained by the marks performed during recording
of the entire acoustic signal.
"""


# Standard library imports
import os
import json
import argparse

# Third party imports
from scipy.io import wavfile

# Local application imports
import dsip.sigproc as dsp


if __name__ == "__main__":

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

    #### READ JSON FILE ####
    with open(input_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    #### PARAMETERS ####
    db_path = dataset[0]['path']
    size = dataset[0]['bubbleLength']
    node = dataset[3]
    name = node['audioName'][:-4]
    audio_path = db_path + node['path'] + node['audioName']

    #### LOADING AUDIO FILE ####
    Fs, wave = wavfile.read(audio_path)

    #### CUTTING SIGNAL THAT MATCHES THE VIDEO ####
    max_values = dsp.get_max_values(wave, size)
    wave_cutted = wave[max_values[0]:max_values[-1]]

    wavfile.write('{}_cut.wav'.format(name), Fs, wave_cutted)
    print('Acoustic Signal Saved!')
