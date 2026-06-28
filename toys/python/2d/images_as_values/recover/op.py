# Treat the raw image pixels as symbols


import numpy as np
import cv2

# bind(shoes, noise)
img_shoes_by_noise = cv2.imread('../output/multi/shoes_by_noise_element.jpg', cv2.IMREAD_GRAYSCALE)

# bind(pen, noise)
img_pen_by_noise = cv2.imread('../output/multi/pen_by_noise_element.jpg', cv2.IMREAD_GRAYSCALE)

# noise
img_noise = cv2.imread('../images/noise.jpg', cv2.IMREAD_GRAYSCALE)




# bundle(bind(shoes, noise), bind(pen, noise))
sum = img_shoes_by_noise + img_pen_by_noise
cv2.imwrite('./bundle.jpg', sum)

# shoes = 2
# pen = 3
# noise = 5
#
# 25 = bundle(bind(2, 5), bind(3, 5))
# 25 = bundle(10, 15)
# 25 = 10 + 15
#
# 25 / noise = (10 / noise) + (15 / noise)
# 5 = 2 + 3

r = sum / img_pen_by_noise
cv2.imwrite(f'./unbound_pen.jpg', r)

r = sum / img_shoes_by_noise
cv2.imwrite(f'./unbound_shoes.jpg', r)

# What's going on here?
# Visually we see artifacts of both pen and shoes in
#  even exponents but not odd ones.
#  Try changing 10 to 128 and comparing recovered images
for exp in range(10):
  r = sum / (img_noise ** exp)
  cv2.imwrite(f'./recovered/{exp:03d}.jpg', r)


