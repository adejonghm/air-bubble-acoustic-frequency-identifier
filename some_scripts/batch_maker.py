#!/usr/bin/env python3

"""
Created on Apr 25, 2019
@author: adejonghm
-----------------------

Script to create the batch file for rename ".wav" file.
Put this file into the same folder that ".txt" file.
"""

import sys
import pandas as pd

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You must pass the "file name" as an argument!')
        sys.exit(1)

    FILE_PATH = sys.argv[1]

    # ****** Loading ******
    DATASET = pd.read_csv(FILE_PATH, sep=" ", header=None)

    # ****** Building ******
    TEXT = []
    # YEAR = MONTH = OTHER = ""
    for i in DATASET[1]:
        year, month, day, hour, minute, seg = i[:4], i[4:6], i[6:8], i[9:11], i[12:14], i[15:17]
        TEXT.append(year + "_" + month + "_" + day + '_' + hour + '_' + minute + '_' + seg + '.wav')

    DATASET[1], DATASET[2], DATASET[0] = DATASET[0], TEXT, 'ren'

    # ****** Writing ******
    pd.DataFrame(DATASET).to_csv('renomeacao.bat', sep=" ", index=False, header=None)
