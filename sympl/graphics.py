'''
Author Martin McBride
Copyright (c) 2018
'''

class Drawable():
    
    def __init__(self,
                 translate=(0, 0)):
        self.translate = translate[:]
        
    def draw(self, ctx):
        pass
        
class Rectangle(Drawable):
    
    def __init__(self,
                 translate=(0, 0),
                 position=(0, 0),
                 width=100,
                 height=100,
                 color=(0, 0, 0)):
        Drawable.__init__(self, translate)
        self.position = position[:]
        self.width = width
        self.height = height
        self.color = color[:]

    def draw(self, ctx):
        ctx.new_path()
        ctx.rectangle(self.position[0], self.position[1], self.width, self.height)
        ctx.set_source_rgb(*self.color)
        ctx.fill()
