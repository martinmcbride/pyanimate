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
        return x*self.extent[0]/self.pixel_size[0]

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
        ctx.scale(self.pixel_size[0]/self.extent[0], -self.pixel_size[1]/self.extent[1])
        ctx.translate(-self.start[0], -(self.start[1]+self.extent[1]))

    def pop(self, ctx):
        ctx.restore()

def fill_stroke(ctx, fill_color=None, line_color=None, line_width=1):
    """
    Fill and or stoke current path
    fill_color of None means no fill
    line_color of None means no stroke
    :param ctx: cairo context
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    if fill_color:
        ctx.set_source_rgb(*fill_color)
        if line_color:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if line_color:
        ctx.set_line_width(line_width)
        ctx.set_source_rgb(*line_color)
        ctx.stroke()

def line(ctx, a, b, line_color=None, line_width=1):
    """
    Draw a line from a to b
    :param ctx: cairo context
    :param a: tuple (x, y) start of line
    :param b: tuple (x, y) end of line
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    ctx.move_to(*a)
    ctx.line_to(*b)
    fill_stroke(ctx, None, line_color, line_width)

def circle(ctx, centre, radius, fill_color=None, line_color=None, line_width=1):
    """
    Draw a circle with centre and radius
    :param ctx: cairo context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    ctx.arc(*centre, radius, 0, 2*math.pi)
    fill_stroke(ctx, fill_color, line_color, line_width)

def arc(ctx, centre, radius, start_angle, end_angle, fill_color=None, line_color=None, line_width=1):
    """
    Draw an arc with centre and radius
    :param ctx: cairo context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param start_angle: start angle of arc, ccw from x axis
    :param end_angle: end angle of arc, ccw from x axis
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    ctx.arc(*centre, radius, start_angle, end_angle)
    fill_stroke(ctx, fill_color, line_color, line_width)

def sector(ctx, centre, radius, start_angle, end_angle, fill_color=None, line_color=None, line_width=1):
    """
    Draw a sector with centre and radius
    :param ctx: cairo context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param start_angle: start angle of arc, ccw from x axis
    :param end_angle: end angle of arc, ccw from x axis
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    ctx.move_to(*centre)
    ctx.arc(*centre, radius, start_angle, end_angle)
    ctx.close_path()
    fill_stroke(ctx, fill_color, line_color, line_width)

def segment(ctx, centre, radius, start_angle, end_angle, fill_color=None, line_color=None, line_width=1):
    """
    Draw a segment with centre and radius
    :param ctx: cairo context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param start_angle: start angle of arc, ccw from x axis
    :param end_angle: end angle of arc, ccw from x axis
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    ctx.arc(*centre, radius, start_angle, end_angle)
    ctx.close_path()
    fill_stroke(ctx, fill_color, line_color, line_width)

def point(ctx, pos, size, fill_color=(0, 0, 0)):
    """
    Draw a point
    :param ctx: cairo context
    :param pos: position of point
    :param size: size of point
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :return:
    """
    ctx.arc(pos[0], pos[1], size, 0, 2*math.pi)
    fill_stroke(ctx, fill_color=fill_color)


def tick(ctx, a, b, size, count=1, line_color=(0, 0, 0), line_width=1):
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

    
