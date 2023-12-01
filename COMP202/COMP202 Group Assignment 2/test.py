from PIL import Image
import numpy as np
from image_proc import *
import sys

FILENAME = "plan1.txt"
WIDTH, HEIGHT = 1024, 768

f = open(FILENAME, "r")
s = f.read
f.close()

show_image(decompress(s), HEIGHT, WIDTH)