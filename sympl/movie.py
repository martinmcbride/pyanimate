'''
Author Martin McBride
Copyright (c) 2018
'''

import cairo

class Scene:
    
    def __init__(self, movie, frames, background=(1, 1, 1)):
        self.movie = movie
        self.frames = frames
        self.background = background
        
    def render(self, start_frame):
        self.setup()
        for i in range(self.frames):
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.movie.width, self.movie.height)
            ctx = cairo.Context(surface)
            
            # Draw background
            ctx.new_path()
            ctx.rectangle(0, 0, self.movie.width, self.movie.height)
            ctx.set_source_rgb(*self.background)
            ctx.fill()
            
            self.draw(ctx, i)
            surface.write_to_png('/tmp/animation/image{:05d}.png'.format(start_frame + i))
            
    def setup(self):
        pass
    
    def draw(self, ctx, frame):
        pass
    

class Movie:
    
    def __init__(self, width=320, height=240):
        self.scenes = []
        self.width = width
        self.height = height
        self.folder = ''
        
    def add_scene(self, scene):
        self.scenes.append(scene)
        
    def render(self, folder):
        self.folder = folder
        frame = 0
        for scene in self.scenes:
            scene.render(frame)
            frame += scene.frames