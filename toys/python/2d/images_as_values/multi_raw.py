import numpy as np
import cv2

img_shoes = cv2.imread('./images/shoes.jpg', cv2.IMREAD_GRAYSCALE)
img_pen = cv2.imread('./images/pen.jpg', cv2.IMREAD_GRAYSCALE)
img_noise = cv2.imread('./images/noise.jpg', cv2.IMREAD_GRAYSCALE)

max_val = 255

# Shoes and Noise
element_wise = img_shoes * img_noise
matrix_wise = img_shoes @ img_noise
cv2.imwrite('./output/multi/shoes_by_noise_element.jpg', element_wise)
cv2.imwrite('./output/multi/shoes_by_noise_matrix.jpg', matrix_wise)

element_wise = (img_shoes * img_noise) % max_val
matrix_wise = (img_shoes @ img_noise) % max_val
cv2.imwrite('./output/multi/shoes_by_noise_element_mod.jpg', element_wise)
cv2.imwrite('./output/multi/shoes_by_noise_matrix_mod.jpg', matrix_wise)

element_wise = img_noise * img_shoes
matrix_wise = img_noise @ img_shoes
cv2.imwrite('./output/multi/noise_by_shoes_element.jpg', element_wise)
cv2.imwrite('./output/multi/noise_by_shoes_matrix.jpg', matrix_wise)

element_wise = (img_noise * img_shoes) % max_val
matrix_wise = (img_noise @ img_shoes) % max_val
cv2.imwrite('./output/multi/noise_by_shoes_element_mod.jpg', element_wise)
cv2.imwrite('./output/multi/noise_by_shoes_matrix_mod.jpg', matrix_wise)



# Pen and Noise
element_wise = img_pen * img_noise
matrix_wise = img_pen @ img_noise
cv2.imwrite('./output/multi/pen_by_noise_element.jpg', element_wise)
cv2.imwrite('./output/multi/pen_by_noise_matrix.jpg', matrix_wise)

element_wise = img_noise * img_pen
matrix_wise = img_noise @ img_pen
cv2.imwrite('./output/multi/noise_by_pen_element.jpg', element_wise)
cv2.imwrite('./output/multi/noise_by_pen_matrix.jpg', matrix_wise)

element_wise = (img_pen * img_noise) % max_val
matrix_wise = (img_pen @ img_noise) % max_val
cv2.imwrite('./output/multi/pen_by_noise_element_mod.jpg', element_wise)
cv2.imwrite('./output/multi/pen_by_noise_matrix_mod.jpg', matrix_wise)

element_wise = (img_noise * img_pen) % max_val
matrix_wise = (img_noise @ img_pen) % max_val
cv2.imwrite('./output/multi/noise_by_pen_element_mod.jpg', element_wise)
cv2.imwrite('./output/multi/noise_by_pen_matrix_mod.jpg', matrix_wise)


# Shoes and Pen
element_wise = img_shoes * img_pen
matrix_wise = img_shoes @ img_pen
cv2.imwrite('./output/multi/shoes_by_pen_element.jpg', element_wise)
cv2.imwrite('./output/multi/shoes_by_pen_matrix.jpg', matrix_wise)

element_wise = img_pen * img_shoes # elementwise multi is commutative
matrix_wise = img_pen @ img_shoes  # matrix multi is non-commutative
cv2.imwrite('./output/multi/pen_by_shoes_element.jpg', element_wise)
cv2.imwrite('./output/multi/pen_by_shoes_matrix.jpg', matrix_wise)

element_wise = (img_shoes * img_pen) % max_val
matrix_wise = (img_shoes @ img_pen) % max_val
cv2.imwrite('./output/multi/shoes_by_pen_element_mod.jpg', element_wise)
cv2.imwrite('./output/multi/shoes_by_pen_matrix_mod.jpg', matrix_wise)

element_wise = (img_pen * img_shoes) % max_val # elementwise multi is commutative
matrix_wise = (img_pen @ img_shoes) % max_val  # matrix multi is non-commutative
cv2.imwrite('./output/multi/pen_by_shoes_element_mod.jpg', element_wise)
cv2.imwrite('./output/multi/pen_by_shoes_matrix_mod.jpg', matrix_wise)
