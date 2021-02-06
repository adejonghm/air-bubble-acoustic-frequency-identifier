#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Script to separate a video frame by frame. It's necessary to provide
the input path as parameter and you could provide the output path as
parameter too. By default create the output folder in the script folder.
"""


# Standard library imports
from os import sys, makedirs
# import shutil

# Third party imports
import cv2 as cv


def get_info(videofile):
    """[summary]

    Args:
        videofile ([type]): [description]
    """

    fps = videofile.get(cv.CAP_PROP_FPS)
    frame_count = int(videofile.get(cv.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    minutes = int(duration / 60)
    seconds = duration % 60

    print('-------')
    print('FPS: {}'.format(fps))
    print('Number of Frames: {}'.format(frame_count))
    print('Duration(M:S): {}:{}'.format(minutes, seconds))

    videofile.release()


if __name__ == '__main__':

    args = sys.argv
    if len(args) < 3:
        print('Missing arguments! Expected 2 argumens and receive {}.\n'
              'Example:\n  {} <input_path> <output_path>'.
              format(len(args) - 1, args[0]))
        sys.exit(1)

    input_path = args[1]
    output_path = args[2] if args[2].endswith('/') else args[2] + '/'

    # ****** Loading video ******
    formtas = ('avi', 'mp4', 'mkv', 'mpg')
    if input_path.endswith(formtas):
        video = cv.VideoCapture(input_path)
    else:
        print("Invalid Video Format! Valid formats {}".format(formtas))
        sys.exit(1)

    # ****** Creating output folder ******
    makedirs(output_path, exist_ok=True)

    step = 0
    flag = True
    while flag:
        if step == 0:
            print('Creating...')

        # ****** Reading video frames ******
        flag, frame = video.read()      # devuelve ndarray con los tres canales

        # ****** Writing video frames ******
        name = output_path + 'frame_' + str(step+1) + '.jpg'
        if flag:
            cv.imwrite(name, frame)
            step += 1

    # ****** releasing video ******
    video.release()
    cv.destroyAllWindows()
    print('DONE! {} frames generated'.format(step))
