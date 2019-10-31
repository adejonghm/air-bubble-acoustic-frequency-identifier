#!/usr/bin/env python3

"""
Created on Apr 25, 2019
@author: adejonghm
-----------------------

Script to rename ".wav" files.
Put this file together with the folder that contains ".wav" files.
"""

import os
import sys
import pandas as pd


def make_date(data):
    """ No Description """
    if data[0].isdigit():
        data = data.split('_')
        data[0] = data[0][0:4] + '_' + data[0][4:6] + '_' + data[0][6:]
        for i in data[1]:
            if i == 's':
                data[1] = data[1].replace(i, '.wav')
            if i in ('h', 'm'):
                data[1] = data[1].replace(i, '_')
        return data[0] + '_' + data[1]
    return data


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('You must pass the "folder path" and the "rename file" as arguments!')
        print('Example: python rename.py test/ rename.txt')
        sys.exit(1)

    elif len(sys.argv) == 2:
        print('One of the arguments is missing "folder" or "rename file"!')
        sys.exit(1)

    else:
        PATH = sys.argv[1]
        SOURCE = sys.argv[2]
        FILE = pd.read_csv(PATH+SOURCE, sep=" ", header=None)
        FILE_LIST = sorted(os.listdir(PATH))

        for item in range(len(FILE_LIST) - 1):
            src = PATH + FILE[0][item]
            date = make_date(FILE[1][item])
            dst = PATH + date
            os.rename(src, dst)

        print('DONE!')
