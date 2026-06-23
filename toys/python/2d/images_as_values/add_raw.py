import numpy as np
import cv2

img_shoes = cv2.imread('./images/shoes.jpg', cv2.IMREAD_GRAYSCALE)
img_pen = cv2.imread('./images/pen.jpg', cv2.IMREAD_GRAYSCALE)
img_noise = cv2.imread('./images/noise.jpg', cv2.IMREAD_GRAYSCALE)

max_val = 255

# Shoes and Noise
sum = img_shoes + img_noise
average = (img_shoes + img_noise) / 2
cv2.imwrite('./output/add/shoes_by_noise_sum.jpg', sum)
cv2.imwrite('./output/add/shoes_by_noise_average.jpg', average)

sum = img_noise + img_shoes
average = (img_noise + img_shoes) / 2
cv2.imwrite('./output/add/noise_by_shoes_sum.jpg', sum)
cv2.imwrite('./output/add/noise_by_shoes_average.jpg', average)

modsum = (img_shoes + img_noise) % max_val
cv2.imwrite('./output/add/shoes_by_noise_modsum.jpg', modsum)


# Pen and Noise
sum = img_pen + img_noise
average = (img_pen + img_noise) / 2
cv2.imwrite('./output/add/pen_by_noise_sum.jpg', sum)
cv2.imwrite('./output/add/pen_by_noise_average.jpg', average)

sum = img_noise + img_pen
average = (img_noise + img_pen) / 2
cv2.imwrite('./output/add/noise_by_pen_sum.jpg', sum)
cv2.imwrite('./output/add/noise_by_pen_average.jpg', average)

modsum = (img_pen + img_noise) % max_val
cv2.imwrite('./output/add/pen_by_noise_modsum.jpg', modsum)

# Shoes and Pen
sum = img_shoes + img_pen
average = (img_shoes + img_pen) / 2
cv2.imwrite('./output/add/shoes_by_pen_sum.jpg', sum)
cv2.imwrite('./output/add/shoes_by_pen_average.jpg', average)

modsum = (img_shoes + img_pen) % max_val
cv2.imwrite('./output/add/shoes_by_pen_modsum.jpg', modsum)
