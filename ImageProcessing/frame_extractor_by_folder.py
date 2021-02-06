#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------


"""


# Standard library imports
import csv
import os
import shutil

# Third party imports
import cv2 as cv


def separate(in_path, out_path):
    """
    Arguments:
        in_path {[type]} -- [description]
        out_path {[type]} -- [description]
    """
    vid = cv.VideoCapture(in_path)
    number_frames = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
    fps = int(round(vid.get(cv.CAP_PROP_FPS), 0))
    length = number_frames

    if number_frames % fps != 0:
        time = number_frames // fps
        length = time * fps

    for i in range(length):
        factor = len(str(length))

        # ****** Reading video frames ******
        _, frame = vid.read()

        # ****** Creating names ******
        if i < 9:
            name = '0'*(factor-1) + str(i+1) + '.jpg'
        elif i >= 9 and i < 99:
            name = '0'*(factor-2) + str(i+1) + '.jpg'
        elif i >= 99 and i < 999:
            name = '0'*(factor-3) + str(i+1) + '.jpg'
        elif i >= 999 and i < 9999:
            name = '0'*(factor-4) + str(i+1) + '.jpg'
        elif i >= 9999 and i < 99999:
            name = '0'*(factor-5) + str(i+1) + '.jpg'
        else:
            name = str(i+1) + '.jpg'

        # ****** Writing video frames ******
        cv.imwrite(out_path + name, frame)

    # ****** Releasing video ******
    vid.release()
    cv.destroyAllWindows()


if __name__ == '__main__':

    # ****** Loading video ******
    args = len(os.sys.argv)
    if args < 3:
        print('Missing arguments! Expected 2 argumens and receive {}.'
              'Example:\n  {} <input_path> <output_path>'.
              format(args-1, os.sys.argv[0]))
        os.sys.exit(1)

    formtas = ('avi', 'mp4', 'mkv', 'mpg')
    input_path = os.sys.argv[1]
    if input_path.endswith(formtas):
        video = cv.VideoCapture(input_path)
    else:
        print("Invalid Video Format! Valid formats {}".format(formtas))
        os.sys.exit(1)

    # ****** Creating output_path folder ******
    output_path = os.sys.argv[2] if os.sys.argv[2].endswith(
        '/') else os.sys.argv[2] + '/'
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
        os.makedirs(output_path)
    else:
        os.makedirs(output_path)

    # ****** Creating a list with the names of video files ******
    filenames = []
    for row in sorted(os.listdir(input_path)):
        if '.avi' in row:
            filenames.append(row.split('.avi')[0])

    # ****** Loading CSV File ******
    with open(input_path + 'measurements.csv', encoding='utf-8') as openfile:
        readfile = csv.reader(openfile)

    index = 0
    for row in readfile:
        NAME = (row[2].split('_'))[1] + '_' + 'd' + row[0] + '_' + 'fps' + row[1]

        if filenames[index] in row:
            temporal_path = output_path + NAME
            os.makedirs(temporal_path)
            video = input_path + filenames[index] + '.avi'
            separate(video, temporal_path)
            index += 1
