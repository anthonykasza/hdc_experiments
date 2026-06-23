import numpy as np
import cv2

from embedding import embed

img_shoes = embed(cv2.imread('./images/shoes.jpg', cv2.IMREAD_GRAYSCALE))
img_pen = embed(cv2.imread('./images/pen.jpg', cv2.IMREAD_GRAYSCALE))
img_noise = embed(cv2.imread('./images/noise.jpg', cv2.IMREAD_GRAYSCALE))

# Shoes and Noise
sum = img_shoes + img_noise
average = (img_shoes + img_noise) / 2
cv2.imwrite('./output/add/shoes_by_noise_sum_embed.jpg', sum)
cv2.imwrite('./output/add/shoes_by_noise_average_embed.jpg', average)

sum = img_noise + img_shoes
average = (img_noise + img_shoes) / 2
cv2.imwrite('./output/add/noise_by_shoes_sum_embed.jpg', sum)
cv2.imwrite('./output/add/noise_by_shoes_average_embed.jpg', average)


# Pen and Noise
sum = img_pen + img_noise
average = (img_pen + img_noise) / 2
cv2.imwrite('./output/add/pen_by_noise_sum_embed.jpg', sum)
cv2.imwrite('./output/add/pen_by_noise_average_embed.jpg', average)

sum = img_noise + img_pen
average = (img_noise + img_pen) / 2
cv2.imwrite('./output/add/noise_by_pen_sum_embed.jpg', sum)
cv2.imwrite('./output/add/noise_by_pen_average_embed.jpg', average)

# Shoes and Pen
sum = img_shoes + img_pen
average = (img_shoes + img_pen) / 2
cv2.imwrite('./output/add/shoes_by_pen_sum_embed.jpg', sum)
cv2.imwrite('./output/add/shoes_by_pen_average_embed.jpg', average)
