import numpy as np
from PIL import Image

def make_uniform_noise_image(width=512, height=512, seed=None, filename="noise_u.jpg"):
  if seed is not None:
    np.random.seed(seed)
  img_array = np.random.randint(0, 256, size=(height, width), dtype=np.uint8)
  img = Image.fromarray(img_array, mode="L")
  img.save(filename, quality=95)
  return img

make_uniform_noise_image()
