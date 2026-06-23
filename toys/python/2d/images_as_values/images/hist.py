import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter


img_noise = cv2.imread('./noise.jpg', cv2.IMREAD_GRAYSCALE)
c = Counter(img_noise.flatten())

# Noise is approximately a gaussian, 0 and 255 are over represented
plt.bar(c.keys(), c.values())
plt.show()


img_shoes = cv2.imread('./shoes.jpg', cv2.IMREAD_GRAYSCALE)
c = Counter(img_shoes.flatten())

plt.bar(c.keys(), c.values())
plt.show()


img_pen = cv2.imread('./pen.jpg', cv2.IMREAD_GRAYSCALE)
c = Counter(img_pen.flatten())

plt.bar(c.keys(), c.values())
plt.show()
