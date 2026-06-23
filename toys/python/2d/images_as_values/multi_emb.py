import numpy as np
import cv2

from embedding import embed

img_shoes = embed(cv2.imread('./images/shoes.jpg', cv2.IMREAD_GRAYSCALE))
img_pen = embed(cv2.imread('./images/pen.jpg', cv2.IMREAD_GRAYSCALE))
img_noise = embed(cv2.imread('./images/noise.jpg', cv2.IMREAD_GRAYSCALE))


# Shoes and Noise
element_wise = img_shoes * img_noise
matrix_wise = img_shoes @ img_noise
cv2.imwrite('./output/multi/shoes_by_noise_element_embed.jpg', element_wise)
cv2.imwrite('./output/multi/shoes_by_noise_matrix_embed.jpg', matrix_wise)

element_wise = img_noise * img_shoes
matrix_wise = img_noise @ img_shoes
cv2.imwrite('./output/multi/noise_by_shoes_element_embed.jpg', element_wise)
cv2.imwrite('./output/multi/noise_by_shoes_matrix_embed.jpg', matrix_wise)


# Pen and Noise
element_wise = img_pen * img_noise
matrix_wise = img_pen @ img_noise
cv2.imwrite('./output/multi/pen_by_noise_element_embed.jpg', element_wise)
cv2.imwrite('./output/multi/pen_by_noise_matrix_embed.jpg', matrix_wise)

element_wise = img_noise * img_pen
matrix_wise = img_noise @ img_pen
cv2.imwrite('./output/multi/noise_by_pen_element_embed.jpg', element_wise)
cv2.imwrite('./output/multi/noise_by_pen_matrix_embed.jpg', matrix_wise)


# Shoes and Pen
element_wise = img_shoes * img_pen
matrix_wise = img_shoes @ img_pen
cv2.imwrite('./output/multi/shoes_by_pen_element_embed.jpg', element_wise)
cv2.imwrite('./output/multi/shoes_by_pen_matrix_embed.jpg', matrix_wise)

element_wise = img_pen * img_shoes # elementwise multi is commutative
matrix_wise = img_pen @ img_shoes  # matrix multi is non-commutative
cv2.imwrite('./output/multi/pen_by_shoes_element_embed.jpg', element_wise)
cv2.imwrite('./output/multi/pen_by_shoes_matrix_embed.jpg', matrix_wise)
