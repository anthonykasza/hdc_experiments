import numpy as np
import cv2

from qhrr import *


def embed_image(image):
  """
  Bag-of-pixels encoder
  """
  pixels = []

  for y in range(height):
    for x in range(width):
      pixels.append(
        bind(
          position_hvs[y][x],
          vals[int(image[y, x])]
        )
      )

  return bundle(pixels)


# -------------------------------------------------------
# Parameters
# -------------------------------------------------------

dims = 1024
max_px_pos = 512
max_val = 256
num_trials = 5

clean_path = "../2d/images_as_values/output/levels/pen_to_noise_000.jpg"
noisyhalf_path = "../2d/images_as_values/output/levels/pen_to_noise_004.jpg"
noisyfull_path = "../2d/images_as_values/output/levels/pen_to_noise_009.jpg"

img = cv2.imread(clean_path, cv2.IMREAD_GRAYSCALE)
img_noisyhalf = cv2.imread(noisyhalf_path, cv2.IMREAD_GRAYSCALE)
img_noisyfull = cv2.imread(noisyfull_path, cv2.IMREAD_GRAYSCALE)

height, width = img.shape

clean_half_sims = []
clean_full_sims = []
half_full_sims = []


# -------------------------------------------------------
# Run trials
# -------------------------------------------------------

for trial in range(num_trials):
  print(f"\nTrial {trial + 1}/{num_trials}")
  print(f"\tgenerating symbols")

  x_pos = [new_hv(dims) for _ in range(max_px_pos)]
  y_pos = [new_hv(dims) for _ in range(max_px_pos)]

  position_hvs = [
    [bind(x_pos[x], y_pos[y]) for x in range(width)]
    for y in range(height)
  ]

  val_basis = new_hv(dims)
  vals = [
    fraction_power_encoding(val_basis, i / (max_val - 1))
    for i in range(max_val)
  ]

  # -------------------------------------------------------
  # Embed images
  # -------------------------------------------------------

  print(f"\tembedding images")
  clean_hv = embed_image(img)
  noisyhalf_hv = embed_image(img_noisyhalf)
  noisyfull_hv = embed_image(img_noisyfull)

  # -------------------------------------------------------
  # Compute similarities
  # -------------------------------------------------------

  clean_half_sims.append(similarity(clean_hv, noisyhalf_hv))
  clean_full_sims.append(similarity(clean_hv, noisyfull_hv))
  half_full_sims.append(similarity(noisyhalf_hv, noisyfull_hv))

# -------------------------------------------------------
# Average results
# -------------------------------------------------------

print("\nAverage similarities over", num_trials, "trials:")
print(f"Clean to half-noise    : {np.mean(clean_half_sims):.6f}")
print(f"Clean to full-noise    : {np.mean(clean_full_sims):.6f}")
print(f"Half-noise to full-noise : {np.mean(half_full_sims):.6f}")
