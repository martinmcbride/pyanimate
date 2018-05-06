'''
Author Martin McBride
Copyright (c) 2018
'''

import cairo

class Scene:
    
    def __init__(self, movie, frames):
        self.movie = movie
        self.frames = frames
        
    def render(self, start_frame):
        self.setup()
        for i in range(self.frames):
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.movie.width, self.movie.height)
            ctx = cairo.Context(surface)
            self.draw(ctx, i)
            surface.write_to_png('image' + str(start_frame + i) + '.png')
            
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