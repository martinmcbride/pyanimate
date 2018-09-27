# Author:  Martin McBride
# Created: 2018-09-22
# Copyright (C) 2018, Martin McBride
# License: MIT


import imageio
import subprocess


def save_animated_gif(filepath, frames, delay, loop=0):
    if not filepath.lower().endswith('.gif'):
        filepath += '.gif'
    images = list(frames)
    imageio.mimsave(filepath, images, duration=delay)
    subprocess.run(['gifsicle', '-b', '--colors', '256', filepath])


