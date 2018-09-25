import cairo
import numpy as np
import math


class Axes:
    def __init__(self, coords, divisions=(1, 1)):
        self.coords = coords
        self.divisions = divisions


    def draw_axes(self, ctx):
        for p in self.get_divs(self.coords.start[0], self.coords.extent[0], self.divisions[0]):
            ctx.move_to(*self.coords.c2p((p, self.coords.start[1])))
            ctx.line_to(*self.coords.c2p((p, self.coords.start[1]+self.coords.extent[1])))
        for p in self.get_divs(self.coords.start[1], self.coords.extent[1], self.divisions[1]):
            ctx.move_to(*self.coords.c2p((self.coords.start[0], p)))
            ctx.line_to(*self.coords.c2p((self.coords.start[0]+self.coords.extent[0], p)))
        ctx.set_source_rgb(.5, .5, 1)
        ctx.set_line_width(2)
        ctx.stroke()

        ctx.set_source_rgb(0.1, 0.1, 0.1)
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(15)
        for p in self.get_divs(self.coords.start[0], self.coords.extent[0], self.divisions[0]):
            if abs(p)>0.001:
                pstr = str(round(p*1000)/1000)
                ppx = self.coords.c2p((p, 0))
                x, y, width, height, dx, dy = ctx.text_extents(pstr)
                ctx.move_to(ppx[0]-width-4, ppx[1]+height+4)
                ctx.show_text(pstr)
        for p in self.get_divs(self.coords.start[1], self.coords.extent[1], self.divisions[1]):
            if abs(p)>0.001:
                pstr = str(round(p*1000)/1000)
                ppx = self.coords.c2p((0, p))
                x, y, width, height, dx, dy = ctx.text_extents(pstr)
                ctx.move_to(ppx[0]-width-4, ppx[1]+height+4)
                ctx.show_text(pstr)

        ctx.move_to(*self.coords.c2p((self.coords.start[0], 0)))
        ctx.line_to(*self.coords.c2p((self.coords.start[0]+self.coords.extent[0], 0)))
        ctx.move_to(*self.coords.c2p((0, self.coords.start[1])))
        ctx.line_to(*self.coords.c2p((0, self.coords.start[1]+self.coords.extent[1])))
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(2)
        ctx.stroke()
        p = self.coords.c2p((0, 0))
        ctx.arc(p[0], p[1], 8, 0, 2*math.pi)
        ctx.stroke()

    def get_divs(self, start, extent, div):
        divs = []
        n = math.ceil(start/div)*div
        while n <= start + extent:
            divs.append(n)
            n += div
        return divs

def plot_curve(ctx, fn, coords, color=(1, 0, 0), extent=None, lw=3):
    points = []
    for x in np.linspace(coords.start[0], coords.start[0]+coords.extent[0], 100):
        if not extent or extent[0] < x < extent[1]:
            points.append((x, fn(x)))
    if points:
        ctx.move_to(*coords.c2p(points[0]))
        for p in points[1:]:
            ctx.line_to(*coords.c2p(p))
    ctx.set_source_rgb(*color)
    ctx.set_line_width(lw)
    ctx.stroke()
 

def plot_yx_curve(ctx, fn, coords, color=(1, 0, 0), extent=None, lw=3):
    points = []
    for y in np.linspace(coords.start[1], coords.start[1]+coords.extent[1], 100):
        if not extent or extent[0] < y < extent[1]:
            points.append((fn(y), y))
    if points:
        ctx.move_to(*coords.c2p(points[0]))
        for p in points[1:]:
            ctx.line_to(*coords.c2p(p))
    ctx.set_source_rgb(*color)
    ctx.set_line_width(lw)
    ctx.stroke()
 

def attribution(ctx, size, text, color=(0.5, 0, 0)):
    ctx.set_source_rgb(*color)
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(20)
    x, y, width, height, dx, dy = ctx.text_extents(text)
    ctx.move_to(size[0]-width-4, size[1]-4)
    ctx.show_text(text)
