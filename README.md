
# Experimental study of air bubble dynamics in water using acoustic analysis and underwater images

> The repository was used during my Master's, in the Acoustics field. The work is focused on the experimental study on the acoustic emission of an underwaterair bubble. Digital Signal Processing techniques are applied in this work and are complemented with some Digital Image Processing techniques.

## Table of Contents

- [Description of the content](#description-of-the-content)
- [How to use this repository](#how-to-use)
- [References](#references)
- [Author Info](#author-info)

---

## Description of the content

### Tools folder

In this folder, there are some scripts that can be used to rename files, wirte a json file, among others.

**bubble_simulation.py**: This script is used to simulate the emission of the acoustic signal of an underwater bubble using the mathematical model proposed by Strasberg [[1]](#references).

**json_manager.py** is used to create and update the JSON file using the library `jilib`.

### SignalProcessing folder

**signal_analysis.py** is used to analyze the acoustic signal emitted by an underwater air bubble. Sound frequency analysis was one of them.

**signal_separator.py** is used to separate each acoustic bubble signal that appears in the acoustic signal analyzed.

**signal_cutter.py** is used to cut the precise time interval obtained by the marks made during the recording of the entire acoustic signal.

**general_analysis.py** is used to jointly analyze the three acoustic signals obtained, for example, to show the average frequency of each acoustic signal, in the same graph.

&nbsp;

![Spectrogam Animation](Tools/spectrogram.png)
  
> Some techniques were applied to achieve the reproduction of the acoustic signal and its respective spectrogram. [Here](https://www.youtube.com/watch?v=XNQIttySj1U) is the video.

&nbsp;

### ImageProcessing folder

**image_segmentation.py** is used to detect and separate the bubble that appears in the image, using the `drlse` methods [[2]](#references), in order to determine some characteristics, such as the volume of the bubble.

Some files can be found in this folder, such as `frame_extractor_by_folder.py`, which is used to separate a set of videos into their respective frames.

There is also the `video_creator.py` script that was developed to create slow-motion videos from a set of images.

**dsip** is a developed module that incorporates its own libraries such as `sigproc`, `improc` and `jilib`, as well as others that are publicly available.

[Back To The Top](#table-of-contents)

---

## How To Use

All the scripts in this repository are developed using Python v3, mainly with the following libraries:

    - JSON (std)
    - Matplotlib (3.3.4)
    - Numpy (1.20.1)
    - OpenCV (4.5.1)
    - OS (std)
    - Pandas (1.2.2)
    - Scikit-Image (0.18.1)
    - Scikit-Learn (0.24.1)
    - Scipy (1.6.1)
    - TQDM (4.58.0)
    -----------------------
    - dsip (0.1a)*

### Installation

(*) This is the developed module that incorporates its own libraries and functions, used in the scripts. It must be copied to some of the addresses included in Python paths to use it. It is strongly recommended to create a virtual environment and copy the module inside it, in the path `/lib/python3.x/site-packages/` to add it to the Python path.

All the libraries used can be installed using PyPI or it can be installed used the `requirements.txt` file.

[Back To The Top](#table-of-contents)

---

## References

[1] Strasberg, M. *Gas bubbles as sources of sound in liquids*. The Journal of the Acoustical Society of America, vol. 28, no. 1, p. 20–26, 1956.

[2] LI, C. & XU, C. & GUI, C. & FOX, M. D. *Distance Regularized Level Set Evolution and Its Application to Image Segmentation*. IEEE Transactions On Image Processing, vol. 19, no. 12, p. 3243-3254, 2010.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4662167.svg)](https://doi.org/10.5281/zenodo.4662167)

[Back To The Top](#table-of-contents)

---

## Author Info

- email: [dejongh.morell@gmail.com](mailto:dejongh.morell@gmail.com)

- LinkedIn: [adejonghm](https://www.linkedin.com/in/adejonghm/)

- Telegram: [adejonghm](https://t.me/adejonghm)

- CodersRank: [adejonghm](https://profile.codersrank.io/user/adejonghm/)

[Back To The Top](#table-of-contents)
