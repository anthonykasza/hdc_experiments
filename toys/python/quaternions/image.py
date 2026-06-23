import numpy as np
import cv2

from qhrr import *

# -------------------------------------------------------
# Parameters
# -------------------------------------------------------

dims = 512

pen_path   = "../2d/images_as_values/output/levels/pen_to_noise_000.jpg" #pen image
noisy_path = "../2d/images_as_values/output/levels/pen_to_noise_000.jpg" #itself
noisy_path = "../2d/images_as_values/output/levels/pen_to_noise_004.jpg" #half noisy
noisy_path = "../2d/images_as_values/output/levels/pen_to_noise_009.jpg" #full noisy

img = cv2.imread(pen_path, cv2.IMREAD_GRAYSCALE)
img_noisy = cv2.imread(noisy_path, cv2.IMREAD_GRAYSCALE)

if img is None:
  raise FileNotFoundError(pen_path)

if img_noisy is None:
  raise FileNotFoundError(noisy_path)

if img.shape != img_noisy.shape:
  raise ValueError("Images must have identical dimensions.")

height, width = img.shape

max_pos = max(height, width)
max_val = 256

# -------------------------------------------------------
# Shared symbol dictionaries
# -------------------------------------------------------

print("Building symbol dictionaries...")

x_pos = [new_hv(dims) for _ in range(max_pos)]
y_pos = [new_hv(dims) for _ in range(max_pos)]

position_hvs = [
  [bind(x_pos[x], y_pos[y]) for x in range(width)]
  for y in range(height)
]

val_basis = new_hv(dims)
vals = [
  fraction_power_encoding(val_basis, i / (max_val - 1))
  for i in range(max_val)
]


def embed_image(image):
  """
  Returns:
    position-keyed embedding,
    row+column embedding,
    hierarchical embedding
  """

  ####################################################
  # 1. Position-keyed pixels
  ####################################################

  pixels = []

  for y in range(height):
    for x in range(width):

      pixels.append(
        bind(
          position_hvs[y][x],
          vals[int(image[y, x])]
        )
      )

  img_hv_pixels = bundle(pixels)

  ####################################################
  # Row embeddings
  ####################################################

  row_val_seqs = []

  for y in range(height):

    row_seq = vals[int(image[y, 0])]

    for x in range(1, width):
      row_seq = bind(row_seq, vals[int(image[y, x])])

    row_val_seqs.append(
      bind(row_seq, y_pos[y])
    )

  ####################################################
  # Column embeddings
  ####################################################

  col_val_seqs = []

  for x in range(width):

    col_seq = vals[int(image[0, x])]

    for y in range(1, height):
      col_seq = bind(col_seq, vals[int(image[y, x])])

    col_val_seqs.append(
      bind(col_seq, x_pos[x])
    )

  ####################################################
  # 2. Bundle rows + columns
  ####################################################

  img_hv_rows_cols = bundle(
    row_val_seqs + col_val_seqs
  )

  ####################################################
  # 3. Hierarchical bundle
  ####################################################

  img_hv_hierarchical = bundle([
    bundle(row_val_seqs),
    bundle(col_val_seqs),
  ])

  return (
    img_hv_pixels,
    img_hv_rows_cols,
    img_hv_hierarchical,
  )


print("Embedding clean image...")
clean_pixels, clean_rows_cols, clean_hier = embed_image(img)

print("Embedding noisy image...")
noisy_pixels, noisy_rows_cols, noisy_hier = embed_image(img_noisy)

# -------------------------------------------------------
# Similarity comparison
# -------------------------------------------------------

print("\nSimilarity (clean vs noisy)")
print("-" * 40)

print(f"Position-keyed : {similarity(clean_pixels, noisy_pixels):.6f}")
print(f"Rows + Columns : {similarity(clean_rows_cols, noisy_rows_cols):.6f}")
print(f"Hierarchical   : {similarity(clean_hier, noisy_hier):.6f}")
