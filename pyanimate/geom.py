import numpy as np
import math
import cairo


class MathsContext:
    """
    Holds the maths coordinate system, where shapes and graphs are defined
    This maps maths coordinates onto pixel coordinates
    """

    def __init__(self, ctx, pixel_size, start, extent):
        """
        Initialise
        :param pixel_size: pixel dimensions of space tuple (width, height)
        :param start: bottom left position in maths coordinates, tuple (x, y)
        :param extent: size in maths coordinates, tuple (width, height)
        """
        self.ctx = ctx
        self.pixel_size = pixel_size
        self.start = start
        self.extent = extent

    def l2m(self, x):
        """
        Convert a size in pixels to a length in math space.
        Only uses x scaling
        :param x: pixel length
        :return: length in maths space
        """
        return x*self.extent[0]/self.pixel_size[0]

    def l2pg(self, x):
        """
        Convert a size in pixels to a length in page space.
        Only uses x scaling
        :param x: pixel length
        :return: length in page space
        """
        return x*100/self.pixel_size[0]

    def pg2l(self, x):
        """
        Convert a length in page space to pixels.
        Only uses x scaling
        :param x: length in page space
        :return:  pixel length
        """
        return x*self.pixel_size[0]/100

    def cm2p(self, pos):
        """
        Convert coordinate position in maths space to pixel position
        :param pos: position in maths space, tuple (x, y)
        :return: position in pixel space, tuple (x, y)
        """
        px = (pos[0] - self.start[0]) * self.pixel_size[0] / self.extent[0]
        py = self.pixel_size[1] - (pos[1] - self.start[1]) * self.pixel_size[1] / self.extent[1]
        return px, py

    def cpg2p(self, pos):
        """
        Convert coordinate position in page space to pixel position
        :param pos: position in maths space, tuple (x, y)
        :return: position in pixel space, tuple (x, y)
        """
        px = pos[0] * self.pixel_size[0] / 100
        py = self.pixel_size[1] - pos[1] * self.pixel_size[0] / 100
        return px, py

    def push_maths(self):
        self.ctx.save()
        self.ctx.scale(self.pixel_size[0]/self.extent[0], -self.pixel_size[1]/self.extent[1])
        self.ctx.translate(-self.start[0], -(self.start[1]+self.extent[1]))

    def push_page(self):
        self.ctx.save()
        self.ctx.scale(self.pixel_size[0]/100, - self.pixel_size[0]/100)
        self.ctx.translate(0, -100*self.pixel_size[1]/self.pixel_size[0])

    def pop(self):
        self.ctx.restore()


def fill_stroke(mctx, fill_color=None, line_color=None, line_width=1):
    """
    Fill and or stoke current path
    fill_color of None means no fill
    line_color of None means no stroke
    :param mctx: maths context
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    if fill_color:
        mctx.ctx.set_source_rgb(*fill_color)
        if line_color:
            mctx.ctx.fill_preserve()
        else:
            mctx.ctx.fill()
    if line_color:
        mctx.ctx.set_line_width(line_width)
        mctx.ctx.set_source_rgb(*line_color)
        mctx.ctx.stroke()


def line(mctx, a, b, line_color=None, line_width=1):
    """
    Draw a line from a to b
    :param mctx: maths context
    :param a: tuple (x, y) start of line
    :param b: tuple (x, y) end of line
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    mctx.push_maths()
    mctx.ctx.move_to(*a)
    mctx.ctx.line_to(*b)
    mctx.pop()
    mctx.push_page()
    fill_stroke(mctx, None, line_color, line_width)
    mctx.pop()


def circle(mctx, centre, radius, fill_color=None, line_color=None, line_width=1):
    """
    Draw a circle with centre and radius
    :param mctx: maths context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    mctx.push_maths()
    mctx.ctx.arc(*centre, radius, 0, 2*math.pi)
    mctx.pop()
    mctx.push_page()
    fill_stroke(mctx, fill_color, line_color, line_width)
    mctx.pop()


def arc(mctx, centre, radius, start_angle, end_angle, fill_color=None, line_color=None, line_width=1):
    """
    Draw an arc with centre and radius
    :param mctx: maths context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param start_angle: start angle of arc, ccw from x axis
    :param end_angle: end angle of arc, ccw from x axis
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    mctx.push_maths()
    mctx.ctx.arc(*centre, radius, start_angle, end_angle)
    mctx.pop()
    mctx.push_page()
    fill_stroke(mctx, fill_color, line_color, line_width)
    mctx.pop()


def sector(mctx, centre, radius, start_angle, end_angle, fill_color=None, line_color=None, line_width=1):
    """
    Draw a sector with centre and radius
    :param mctx: maths context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param start_angle: start angle of arc, ccw from x axis
    :param end_angle: end angle of arc, ccw from x axis
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke
    :return:
    """
    mctx.push_maths()
    mctx.ctx.move_to(*centre)
    mctx.ctx.arc(*centre, radius, start_angle, end_angle)
    mctx.ctx.close_path()
    mctx.pop()
    mctx.push_page()
    fill_stroke(mctx, fill_color, line_color, line_width)
    mctx.pop()


def segment(mctx, centre, radius, start_angle, end_angle, fill_color=None, line_color=None, line_width=1):
    """
    Draw a segment with centre and radius
    :param mctx: maths context
    :param centre: tuple (x, y) centre of circle
    :param radius: radius of circle
    :param start_angle: start angle of arc, ccw from x axis
    :param end_angle: end angle of arc, ccw from x axis
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :param line_color: line color (r, g, b) each channel in range 0.0 to 1.0
    :param line_width: width of stroke in page units
    :return:
    """
    mctx.push_maths()
    mctx.ctx.arc(*centre, radius, start_angle, end_angle)
    mctx.ctx.close_path()
    mctx.pop()
    mctx.push_page()
    fill_stroke(mctx, fill_color, line_color, line_width)
    mctx.pop()


def point(mctx, pos, size, fill_color=(0, 0, 0)):
    """
    Draw a point
    :param mctx: maths context
    :param pos: position of point in maths coords
    :param size: size of point in page units
    :param fill_color: fill color (r, g, b) each channel in range 0.0 to 1.0
    :return:
    """
    p = mctx.cm2p(pos)
    s = mctx.pg2l(size)
    mctx.ctx.arc(p[0], p[1], s, 0, 2*math.pi)
    fill_stroke(mctx, fill_color=fill_color)


def label(mctx, pos, size, text, fill_color=(0, 0, 0)):
    mctx.push_maths()
    mctx.ctx.move_to(*pos)
    mctx.pop()
    mctx.push_page()
    mctx.ctx.scale(1, -1)
    mctx.ctx.set_source_rgb(*fill_color)
    mctx.ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    mctx.ctx.set_font_size(size)
    mctx.ctx.show_text(text)
    mctx.pop()


def tick(mctx, a, b, size, count=1, line_color=(0, 0, 0), line_width=1):
    """
    Draw a tick on a the line ab

    Draws a line half way along the line ab, at right angles
    to it.
    :param mctx: maths context
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
        mctx.ctx.move_to(*d)
        mctx.ctx.line_to(*e)

    ctx.set_source_rgb(*line_color)
    ctx.set_line_width(line_width)
    ctx.fill()

    
