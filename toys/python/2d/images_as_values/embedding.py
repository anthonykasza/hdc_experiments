import numpy as np
import cv2


def embed(img, max_val=255):
  '''Ternary MAP'''
  threshes = [int(max_val / 3), int((max_val / 3) * 2)]
  embedded = np.empty_like(img, dtype=np.int8)

  embedded[img < threshes[0]] = -1
  embedded[(img >= threshes[0]) & (img < threshes[1])] = 0
  embedded[img >= threshes[1]] = 1

  return embedded



if __name__ == '__main__':
  img_noise = cv2.imread('./images/noise.jpg', cv2.IMREAD_GRAYSCALE)
  e = embed(img_noise)

  print('Noise is a good random symbolic hypervector')
  print("dims:", 512*512)
  print("mean:", np.mean(img_noise))
  print("std:", np.std(img_noise))
  print("var:", np.var(img_noise))
  print("norm:", np.linalg.norm(img_noise))
  print(e[0:10])
  print(e[127:127])
  print()


  img_pen = cv2.imread('./images/pen.jpg', cv2.IMREAD_GRAYSCALE)
  e = embed(img_pen)

  print('Is Pen a good random symbolic hypervector?')
  print("dims:", 512*512)
  print("mean:", np.mean(img_pen))
  print("std:", np.std(img_pen))
  print("var:", np.var(img_pen))
  print("norm:", np.linalg.norm(img_pen))
  print(e[0:10])
  print(e[127:127])
  print()
