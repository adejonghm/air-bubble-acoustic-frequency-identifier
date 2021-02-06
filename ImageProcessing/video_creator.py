#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

Create a video from images, it can be in slow motion.
"""


# Standard library imports
from os import listdir, path, sys

# Third party imports
import cv2 as cv
from tqdm import tqdm


if __name__ == "__main__":

    args = sys.argv
    if len(args) < 2:
        print('Missing arguments! Expected 1 argumens and receive {}.'
              'Example:\n  {} <input_path> <output_path>'.
              format(len(args)-1, args[0]))
        sys.exit(1)

    input_path = sys.argv[1] if sys.argv[1].endswith('/') else sys.argv[1] + '/'

    images = []

    for img in sorted(listdir(input_path)):
        if img.endswith('.jpg'):
            images.append(img)

    frame_path = path.join(input_path, images[0])
    frame = cv.imread(frame_path)
    height, width, channels = frame.shape

    fourcc = cv.VideoWriter_fourcc(*'MP4V')
    video = cv.VideoWriter('slow_motion.mp4', fourcc, 20, (width, height))

    for img in tqdm(images):
        temp_path = path.join(input_path, img)
        temp_img = cv.imread(temp_path)
        video.write(temp_img)

    video.release()
    cv.destroyAllWindows()
