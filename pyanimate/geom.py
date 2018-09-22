import numpy as np
import math


class MathsCoords:
    """
    Holds the maths coordinate system, where shapes and graphs are defined
    This maps maths coordinates onto pixel coordinates
    """

    def __init__(self, pixel_size, start, extent):
        """
        Initialise
        :param pixel_size: pixel dimensions of space tuple (width, height)
        :param start: bottom left position in maths coordinates, tuple (x, y)
        :param extent: size in maths coordinates, tuple (width, height)
        """
        self.pixel_size = pixel_size
        self.start = start
        self.extent = extent

    def p2l(self, x):
        """
        Convert a size in pixels to a length in math space.
        Only uses x scaling
        :param x: pixel length
        :return: length in maths space
        """
        return x*self.pixel_size[0]/self.extent[0]

    def c2p(self, pos):
        """
        Convert coordinate position to pixel position
        :param pos: position in maths space, tuple (x, y)
        :return: position in pixel space, tuple (x, y)
        """
        px = (pos[0] - self.start[0]) * self.pixel_size[0] / self.extent[0]
        py = self.pixel_size[1] - (pos[1] - self.start[1]) * self.pixel_size[1] / self.extent[1]
        return px, py

    def push(self, ctx):
        ctx.save()
        #TODO scale and flip

    def pop(self):
        ctx.restore()


def draw_point(ctx, coords, pos, size, color=(0, 0, 0)):
    """
    Draw a point
    :param ctx: context
    :param coords: current maths space
    :param pos: position of point in maths space
    :param size: size of point in pixels
    :param color: color (r, g, b) range 0 to 1
    :return:
    """
    p = coords.c2p(pos)
    ctx.arc(p[0], p[1], size, 0, 2*math.pi)
    ctx.set_source_rgb(*color)
    ctx.fill()


def draw_tick(ctx, a, b, size, count=1, line_color=(0, 0, 0), line_width=1):
    """
    Draw a tick on a the line ab

    Draws a line half way along the line ab, at right angles
    to it.
    :param ctx: context
    :param a: (x, y) tuple point a
    :param b: (x, y) tuple point b
    :param size: length of tick (pixels)
    :param count: number of ticks
    :return: None
    """
    a = np.asarray(a)
    b = np.asarray(b)
    c = (a + b)/2
    c_step = c*size/np.linalg.norm(c)
    ang = math.atan2(b[1]-a[1], b[0]-a[0]) + math.pi/2

    for i in range(count):
        pos = c + c_step*i
        p = coords.c2p(pos)
        d = p[0]+size*math.cos(ang), p[1]+size*math.sin(ang)
        e = p[0]-size*math.cos(ang), p[1]-size*math.sin(ang)
        ctx.move_to(*d)
        ctx.line_to(*e)

    ctx.set_source_rgb(*line_color)
    ctx.set_line_width(line_width)
    ctx.fill()

    
