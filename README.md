
# Experimental study on the acoustic emission of an air bubble in water

> This is the repository used during the development of my Master's carried out in the field of Acoustics and focused on Digital Signal Processing, complemented with Digital Image Processing.

## Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [References](#references)
- [Author Info](#author-info)

## Description

### Scripts folder

In this folder, there are some scripts that can be used to rename files, create an specific .cmd file, among others.

**bubble_simulation.py**: This script is used for the simulation of the acoustic signal emission of a bubble in water using the mathematical model proposed by Strasberg [[1]](#references).

### SignalProcessing folder

**signal_analysis.py** is used to carry out various analyzes on the acoustic signal emitted by a controlled air bubble generated in the water. Sound Frequency analysis was one of them.

**signal_separator.py** is used to separate each bubble that appears in the analyzed acoustic signal, in independent acoustic signals.

**signal_cutter.py** is used to cut the precise time interval obtained by the marks performed during recording of the entire acoustic signal.

**general_analysis.py** is used to carry out some analyzes over the three acoustic signals obtained, for example, show the mean frequency of each acoustic signal, all in the same graph.

**json_manager.py** is used to create and update the JSON file using the library `jilib`.

(*) All these analyzes were performed using the implemented libraries `dsplib` and `jilib`, which are found in the **libs** folder.

&nbsp;

![Spectrogam Animation](spectrogram.jpg)
  
> In this work, some techniques were applied to achieve a reproduction of the acoustic signal on its respective spectrogram. [Here](https://www.youtube.com/watch?v=BDlcL5jpu2w) is the video.

&nbsp;

### ImageProcessing folder

For the images segmentation [[2]](#references)[[3]](#references), **image_segmentation.py** is used to detect and separate the bubble that appears in the image, using some methods (`drlse` and `gfd`), in ordet to determine some characteristics, such as the volume of the bubble.

Some scripts can be found in this folder. **frame_extractor_by_folder.py** is used to separate a set of videos into their respective frames, and **frame_extractor.py** is used to separate a video.

There's also the **video_creator.py** script that was developed to create slow motion videos from a set of images.

(*) All these analyzes were performed using the implemented library `imglib`, which is found in the **libs** folder.

[Back To The Top](#table-of-contents)

## How To Use

All files in this repository are developed using Python v3.6.9, with the following libraries:

    - Scipy (v1.4.1)
    - TQDM (v4.46.0)
    - Numpy (v1.18.4)
    - OpenCV (v3.2.0)*
    - Matplotlib (v3.1.2)
    - Scikit-Image (v0.16.2)
    - JSON (std)
    - OS (std)
<!--- Pillow (v7.1.2)-->

### Installation

(*) This library was installed from the official Ubuntu repository, the rest of the used libraries were installed with PyPI.

[Back To The Top](#table-of-contents)

## References

[1] Strasberg, M. *Gas bubbles as sources of sound in liquids*. The Journal of the Acoustical Society of America, vol. 28, no. 1, p. 20–26, 1956.

[2] LI, C. & XU, C. & GUI, C. & FOX, M. D. *Distance Regularized Level Set Evolution and Its Application to Image Segmentation*. IEEE Transactions On Image Processing, vol. 19, no. 12, p. 3243-3254, 2010.

[3] Zhang, D. & Lu, G. *Shape-based image retrieval using generic Fourier descriptor*. Signal Processing: Image Communication, vol. 17, p. 825–848, 2002

[![DOI](https://zenodo.org/badge/218679128.svg)](https://zenodo.org/badge/latestdoi/218679128)

[Back To The Top](#table-of-contents)

---

## Author Info

- email: dejongh.cu@gmail.com

- LinkedIn: [adejonghm](https://www.linkedin.com/in/adejonghm/)

- CodersRank: [adejonghm](https://profile.codersrank.io/user/adejonghm/)

[Back To The Top](#table-of-contents)
