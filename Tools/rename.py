#!/usr/bin/env python3
# type: ignore

"""
Dev: 	adejonghm
----------

Script to rename ".wav" files.
Put this file together with the folder that contains ".wav" files.
"""

# Standard library imports
import os
import sys

# Third party imports
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
        path = sys.argv[1]
        source = sys.argv[2]
        file = pd.read_csv(path+source, sep=" ", header=None)
        file_list = sorted(os.listdir(path))

        for item in range(len(file_list) - 1):
            src = path + file[0][item]
            date = make_date(file[1][item])
            dst = path + date
            os.rename(src, dst)

        print('DONE!')
