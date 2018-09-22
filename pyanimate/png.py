# Author:  Martin McBride
# Created: 2018-09-22
# Copyright (C) 2018, Martin McBride
# License: MIT

from PIL import Image
import os


def save_png_frames(folder, basename, frames, digits=5):
    """
    Save the frame sequence as a set of individual png images
    :param folder: The folder to save the files
    :param basename: The base filename, not inclduing the .png extension
    :param frames: The sequence of frames
    :param digits: The number of digits to add to the base name
    :return: None
    For example, with a basename of "frame" and 5 digits, the output png files will be called
    frame00000.png, frame00001.png, frame00002.png etc
    """
    for i, frame in enumerate(frames):
        image = Image.fromarray(frame)
        image.save(os.path.join(folder, basename + str(i).zfill(digits) + '.png'))


def save_png_image(filepath, frames):
    """
    Save the first frame of the sequence as a png image
    :param filepath: Full name and path of the file (.png extension optional)
    :param frames: The sequence of frames
    :return:
    """
    if not filepath.lower().endswith('.png'):
        filepath += '.png'
    image = Image.fromarray(next(frames))
    image.save(filepath)
