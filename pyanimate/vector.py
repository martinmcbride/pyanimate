# Author:  Martin McBride
# Created: 2018-09-22
# Copyright (C) 2018, Martin McBride
# License: MIT

import cairo
from PIL import Image
import numpy as np


def make_vector_frames(size, count, draw, **extras):
    """
    Create a set of images and call the draw function on each one. The images are created from a
    cairo context.
    :param size: size in pixels, tuple (wedth, heigh)
    :param count: number of frames to create
    :param draw: function to be called for each frame
    :param **extras: optional extra named parameters that will be passed into the draw function
    :return: Lazy sequence of numpy image buffers

    The draw function is called count times, once for each frame, each time with a new drawing context.
    It accepts the following parameters:
    - ctx the cairo context for drawing
    - size as above
    - count as above
    - index the number of the current frame
    - **extras as above
    """
    for i in range(count):
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, size[0], size[1])
        ctx = cairo.Context(surface)
        ctx.rectangle(0, 0, size[0], size[1])
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
        draw(ctx=ctx, size=size, count=count, index=i, **extras)
        surface.write_to_png('__make_cairo_frames__.png')
        img = Image.open('__make_cairo_frames__.png')
        frame = np.array(img)
        yield (frame)


def make_vector_image(size, draw, **extras):
    """
    Create an image and call the draw function on it. The image is created from a cairo context.
    :param size: size in pixels, tuple (wedth, heigh)
    :param draw: function to be called for each frame
    :param **extras: optional extra named parameters that will be passed into the draw function
    :return: Lazy sequence of numpy image buffers

    The draw function is called count times, once for each frame, each time with a new drawing context.
    It accepts the following parameters:
    - ctx the cairo context for drawing
    - size as above
    - **extras as above
    """
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, size[0], size[1])
    ctx = cairo.Context(surface)
    ctx.rectangle(0, 0, size[0], size[1])
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    draw(ctx=ctx, size=size, **extras)
    surface.write_to_png('__make_cairo_frames__.png')
    img = Image.open('__make_cairo_frames__.png')
    frame = np.array(img)
    yield (frame)

