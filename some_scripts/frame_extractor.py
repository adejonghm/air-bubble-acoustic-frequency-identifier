#!/usr/bin/env python3

"""
Created on Sep 10, 2019
@author: adejonghm
-----------------------

Script to separate a video frame by frame. By default create an output folder
on /home/<user>/Pictures/Frames and it's necessary to provide the video input path.
"""

import os
import shutil
import cv2

if __name__ == '__main__':

    # ****** Creating output folder ******
    if os.path.exists('/home/dejongh/Pictures/Frames/'):
        shutil.rmtree('/home/dejongh/Pictures/Frames/')
        os.makedirs('/home/dejongh/Pictures/Frames/')
    else:
        os.makedirs('/home/dejongh/Pictures/Frames/')

    # ****** Loading video ******
    PATH = input('Enter the full path of the video:')
    VIDEO = cv2.VideoCapture(PATH)

    STEP = 0
    FLAG = True
    while FLAG:
        if STEP == 0:
            print('Creating...')

        # ****** Reading video frames ******
        FLAG, FRAME = VIDEO.read()

        # ****** Writing video frames ******
        NAME = '/home/dejongh/Pictures/Frames/frame_' + str(STEP+1) + '.jpg'
        if FLAG:
            cv2.imwrite(NAME, FRAME)
            STEP += 1

    # ****** releasing video ******
    VIDEO.release()
    cv2.destroyAllWindows()
    print('DONE! {} frames generated'.format(STEP))
