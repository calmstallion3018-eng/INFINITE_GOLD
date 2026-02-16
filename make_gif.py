from PIL import Image
import glob

frames = sorted(glob.glob("frames/*.png"))

images = [Image.open(f) for f in frames]
images[0].save("play.gif", save_all=True, append_images=images[1:], duration=50, loop=0)