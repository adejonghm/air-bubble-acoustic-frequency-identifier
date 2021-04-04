#!/usr/bin/env python3
# type: ignore

"""
Dev: 	adejonghm
----------

Script to create the batch file for rename ".wav" file.
Put this file into the same folder that ".txt" file.
"""

# Standard library imports
import sys

# Third party imports
import pandas as pd


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You must pass the "file name" as an argument!')
        sys.exit(1)

    file_path = sys.argv[1]

    # ****** Loading ******
    dataset = pd.read_csv(file_path, sep=" ", header=None)

    # ****** Building ******
    text = []
    # YEAR = MONTH = OTHER = ""
    for i in dataset[1]:
        year, month, day, hour, minute, seg = i[:4], i[4:6], i[6:8], i[9:11], i[12:14], i[15:17]
        text.append(year + "_" + month + "_" + day + '_' + hour + '_' + minute + '_' + seg + '.wav')

    dataset[1], dataset[2], dataset[0] = dataset[0], text, 'ren'

    # ****** Writing ******
    pd.DataFrame(dataset).to_csv('renomeacao.bat', sep=" ", index=False, header=None)
