from PIL import Image
import os

def save_gif(filename, frames, delay, loop=0):
    images = [Image.fromarray(frame) for frame in frames]
    images[0].save(filename,
               save_all=True,
               append_images=images[1:],
               delay=delay,
               loop=loop)

def save_png(folder, base, frames, zeros=5):
    for i, frame in enumerate(frames):
        image = Image.fromarray(frame)
        image.save(os.path.join(folder, base + str(i).zfill(zeros) + '.png'))

#
# Save the first frame as a single png image
#
def save_png(filename, frames):
    image = Image.fromarray(next(frames))
    image.save(filename + '.png')
