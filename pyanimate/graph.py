import cairo
import numpy as np
import math


class Axes:
    def __init__(self, mctx, divisions=(1, 1)):
        self.mctx = mctx
        self.divisions = divisions


    def draw_axes(self):
        self.mctx.push_maths()
        for p in self.get_divs(self.mctx.start[0], self.mctx.extent[0], self.divisions[0]):
            self.mctx.ctx.move_to(p, self.mctx.start[1])
            self.mctx.ctx.line_to(p, self.mctx.start[1]+self.mctx.extent[1])
        for p in self.get_divs(self.mctx.start[1], self.mctx.extent[1], self.divisions[1]):
            self.mctx.ctx.move_to(self.mctx.start[0], p)
            self.mctx.ctx.line_to(self.mctx.start[0]+self.mctx.extent[0], p)
        self.mctx.pop()
        self.mctx.push_page()
        self.mctx.ctx.set_source_rgb(.5, .5, 1)
        self.mctx.ctx.set_line_width(0.5)
        self.mctx.ctx.stroke()
        self.mctx.pop()

        self.mctx.ctx.set_source_rgb(0.1, 0.1, 0.1)
        self.mctx.ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        self.mctx.ctx.set_font_size(15)

        for p in self.get_divs(self.mctx.start[0], self.mctx.extent[0], self.divisions[0]):
           if abs(p)>0.001:
                pstr = self.format_div(p, self.divisions[0])
                ppx = self.mctx.cm2p((p, 0))
                x, y, width, height, dx, dy = self.mctx.ctx.text_extents(pstr)
                self.mctx.ctx.move_to(ppx[0] - width - 4, ppx[1] + height + 4)
                self.mctx.ctx.show_text(pstr)
        for p in self.get_divs(self.mctx.start[1], self.mctx.extent[1], self.divisions[1]):
            if abs(p)>0.001:
                pstr = self.format_div(p, self.divisions[1])
                ppx = self.mctx.cm2p((0, p))
                x, y, width, height, dx, dy = self.mctx.ctx.text_extents(pstr)
                self.mctx.ctx.move_to(ppx[0]-width-4, ppx[1]+height+4)
                self.mctx.ctx.show_text(pstr)

        self.mctx.push_maths()
        self.mctx.ctx.move_to(self.mctx.start[0], 0)
        self.mctx.ctx.line_to(self.mctx.start[0]+self.mctx.extent[0], 0)
        self.mctx.ctx.move_to(0, self.mctx.start[1])
        self.mctx.ctx.line_to(0, self.mctx.start[1]+self.mctx.extent[1])
        self.mctx.pop()
        p = self.mctx.cm2p((0, 0))
        s = self.mctx.pg2l(3)
        self.mctx.ctx.new_sub_path()
        self.mctx.ctx.arc(p[0], p[1], s, 0, 2*math.pi)
        self.mctx.push_page()
        self.mctx.ctx.set_source_rgb(0, 0, 0)
        self.mctx.ctx.set_line_width(0.5)
        self.mctx.ctx.stroke()
        self.mctx.pop()

    def get_divs(self, start, extent, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= start + extent:
            divs.append(n)
            n += div
        return divs

    def format_div(self, value, div):
        """
        Formats a division value into a string.
        If the division spacing is an integer, the string will be an integer (no dp).
        If the division spacing is float, the string will be a float with a suitable number of decimal places
        :param value: value to be formated
        :param div: division spacing
        :return: string representation of the value
        """
        if isinstance(value, int):
            return str(value)
        return str(round(value*1000)/1000)

def plot_curve(mctx, fn, line_color=(1, 0, 0), extent=None, line_width=.7):
    """
    Plot an y = fn(x)
    :param mctx: maths context
    :param fn: the function, a function object taking 1 number and returning a number
    :param line_color: color of line (r, g, b) each channel in range 0.0 to 1.0
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the x range
    :param line_width: line width in page space
    :return:
    """
    mctx.push_maths()
    points = []
    for x in np.linspace(mctx.start[0], mctx.start[0]+mctx.extent[0], 100):
        if not extent or extent[0] <= x <= extent[1]:
            points.append((x, fn(x)))
    if points:
        mctx.ctx.move_to(*points[0])
        for p in points[1:]:
            mctx.ctx.line_to(*p)
    mctx.pop()
    mctx.push_page()
    mctx.ctx.set_source_rgb(*line_color)
    mctx.ctx.set_line_width(line_width)
    mctx.ctx.stroke()
    mctx.pop()

def plot_yx_curve(mctx, fn, line_color=(1, 0, 0), extent=None, line_width=.7):
    """
    Plot an x = fn(y)
    :param mctx: maths context
    :param fn: the function, a function object taking 1 number and returning a number
    :param line_color: color of line (r, g, b) each channel in range 0.0 to 1.0
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the y range
    :param line_width: line width in page space
    :return:
    """
    mctx.push_maths()
    points = []
    for y in np.linspace(mctx.start[1], mctx.start[1]+mctx.extent[1], 100):
        if not extent or extent[0] <= y <= extent[1]:
            points.append((fn(y), y))
    if points:
        mctx.ctx.move_to(*points[0])
        for p in points[1:]:
            mctx.ctx.line_to(*p)
    mctx.pop()
    mctx.push_page()
    mctx.ctx.set_source_rgb(*line_color)
    mctx.ctx.set_line_width(line_width)
    mctx.ctx.stroke()
    mctx.pop()


def plot_polar_curve(mctx, fn, line_color=(1, 0, 0), extent=None, line_width=.7):
    """
    Plot an r = fn(theta)
    :param mctx: maths context
    :param fn: the function, a function object taking 1 number and returning a number
    :param line_color: color of line (r, g, b) each channel in range 0.0 to 1.0
    :param extent: tuple (start, end) giving extent of curve, or None for the curve to fill the y range
    :param line_width: line width in page space
    :return:
    """
    mctx.push_maths()
    points = []
    for theta in np.linspace(0, 2*math.pi, 100):
        if not extent or extent[0] <= theta <= extent[1]:
            r = fn(theta)
            points.append((r*math.cos(theta), r*math.sin(theta)))
    if points:
        mctx.ctx.move_to(*points[0])
        for p in points[1:]:
            mctx.ctx.line_to(*p)
    mctx.pop()
    mctx.push_page()
    mctx.ctx.set_source_rgb(*line_color)
    mctx.ctx.set_line_width(line_width)
    mctx.ctx.stroke()
    mctx.pop()


def attribution(ctx, size, text, color=(0.5, 0, 0)):
    ctx.set_source_rgb(*color)
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(20)
    x, y, width, height, dx, dy = ctx.text_extents(text)
    ctx.move_to(size[0]-width-4, size[1]-4)
    ctx.show_text(text)
