'''
Author Martin McBride
Copyright (c) 2018
'''

class Tween():
    
    def __init__(self, value=0):
        self.frames = []
        self.previous = value
        
    def set(self, value, frames):
        self.frames.extend([value for i in range(frames)])
        self.previous = value
        return self
        
    def to(self, value, frames):
        self.frames.extend([self.previous + i*(value - self.previous)/frames for i in range(frames)])
        self.previous = value
        return self
        
    def get(self, frame):
        return self.frames[frame] if frame < len(self.frames) else self.previous
        