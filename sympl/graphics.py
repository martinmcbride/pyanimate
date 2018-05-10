'''
Author Martin McBride
Copyright (c) 2018
'''

import cairo

class Drawable():

    BOTTOM_LEFT = 0    
    BOTTOM_CENTRE = 1    
    BOTTOM_RIGHT = 2    
    MIDDLE_LEFT = 3    
    CENTRE = 4
    MIDDLE_RIGHT = 5    
    TOP_LEFT = 6    
    TOP_CENTRE = 7    
    TOP_RIGHT = 8    
    
    def __init__(self,
                 visible=True,
                 alpha=None,
                 cp=(0, 0),
                 translate=(0, 0),
                 scale=None,
                 rotate=None):
        self.visible = visible
        self.alpha = alpha
        self.cp = cp
        self.translate = translate[:]
        self.scale=None
        self.rotate = rotate
        
    def draw(self, ctx):
        pass
    
    def bounds(self, ctx):
        pass
    
    def create_state(self, ctx):
        ctx.save()
        if self.rotate is not None:
            centre = self.get_centre_point(ctx)
            ctx.translate(centre[0], centre[1])
            ctx.rotate(self.rotate)
            ctx.translate(-centre[0], -centre[1])
        
    def restore_state(self, ctx):
        ctx.restore()
        
    def get_centre_point(self, ctx):
        x0, y0, x1, y1 = self.bounds(ctx)
        if self.cp == self.BOTTOM_LEFT:
            return (x0, y0)
        if self.cp == self.BOTTOM_CENTRE:
            return ((x0+x1)/2, y0)
        if self.cp == self.BOTTOM_RIGHT:
            return (x1, y0)
        elif self.cp == self.MIDDLE_LEFT:
            return (x0, (y0+y1)/2)
        if self.cp == self.CENTRE:
            return ((x0+x1)/2, (y0+y1)/2)
        if self.cp == self.MIDDLE_RIGHT:
            return (x1, (y0+y1)/2)
        elif self.cp == self.TOP_LEFT:
            return (x0, y1)
        if self.cp == self.TOP_CENTRE:
            return ((x0+x1)/2, y1)
        if self.cp == self.TOP_RIGHT:
            return (x1, y1)
        else:
            return self.cp
        
        
        
class Rectangle(Drawable):
    
    def __init__(self,
                 visible=True,
                 alpha=None,
                 cp=(0, 0),
                 translate=(0, 0),
                 scale=None,
                 rotate=None,
                 position=(0, 0),
                 width=100,
                 height=100,
                 color=(0, 0, 0)):
        Drawable.__init__(self, visible, alpha, cp, translate, scale, rotate)
        self.position = position[:]
        self.width = width
        self.height = height
        self.color = color[:]

    def draw(self, ctx):
        if self.visible:
            Drawable.create_state(self, ctx)
            ctx.new_path()
            ctx.rectangle(self.position[0], self.position[1], self.width, self.height)
            ctx.set_source_rgb(*self.color)
            ctx.fill()
            Drawable.restore_state(self, ctx)
            
    def bounds(self, ctx):
        return (self.position[0], self.position[1], self.position[0]+self.width, self.position[1]+self.height)

class Text(Drawable):
    
    def __init__(self,
                 visible=True,
                 alpha=None,
                 cp=(0, 0),
                 translate=(0, 0),
                 scale=None,
                 rotate=None,
                 position=(0, 0),
                 text='text',
                 font='ariel',
                 size=16,
                 color=(0, 0, 0)):
        Drawable.__init__(self, visible, alpha, cp, translate, scale, rotate)
        self.position = position[:]
        self.text = text
        self.font = font
        self.size = size
        self.color = color[:]

    def draw(self, ctx):
        if self.visible:
            ctx.select_font_face(self.font,
                                cairo.FONT_SLANT_NORMAL,
                                cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(self.size)
            Drawable.create_state(self, ctx)
            ctx.new_path()
            ctx.move_to(self.position[0], self.position[1])
            ctx.set_source_rgb(*self.color)
            ctx.scale(1, -1) #Draw text right way up
            ctx.show_text(self.text)
            ctx.scale(1, -1)
            Drawable.restore_state(self, ctx)
            
    def bounds(self, ctx):
        x, y, width, height, dx, dy = ctx.text_extents(self.text)
        return (self.position[0], self.position[1], self.position[0]+width, self.position[1]+height)
            
