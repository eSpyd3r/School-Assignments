import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def show_image(image_string, height, width):
    if not all(c in '01' for c in image_string):
        raise ValueError("Only 0s and 1s can be inside the image string.")
    if len(image_string) != height * width:
        raise ValueError("Mismatch between height/width and actual length of image string.")
    arr = np.fromstring(' '.join(image_string), np.uint8, sep=' ').reshape(height, width)
    plt.imshow(arr, cmap="gray")
    plt.show()
show_image('011100', 2, 3)
