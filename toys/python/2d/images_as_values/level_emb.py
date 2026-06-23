import numpy as np
import cv2

from embedding import embed


def make_levels_manhattan(
  levels: int,
  hv1: np.ndarray,
  hv2: np.ndarray,
) -> dict[int, np.ndarray]:
  """
  Generate intermediate hypervectors whose Manhattan distance
  from hv1 increases linearly toward hv2.

  Much faster than performing one random increment at a time.
  """

  hv1 = hv1.astype(np.int16, copy=False)
  hv2 = hv2.astype(np.int16, copy=False)

  delta = hv2 - hv1

  # Coordinates that differ
  idx = np.flatnonzero(delta)

  if len(idx) == 0:
    return {i: hv1.copy() for i in range(levels)}

  # Build a list of all unit Manhattan moves
  #
  # Example:
  # hv1[i]=10, hv2[i]=13
  #
  # contributes:
  #   i, i, i
  #
  # hv1[j]=20, hv2[j]=17
  #
  # contributes:
  #   j, j, j
  #
  counts = np.abs(delta[idx])

  move_indices = np.repeat(idx, counts)
  move_signs = np.repeat(np.sign(delta[idx]), counts)

  total_work = len(move_indices)

  # Randomize order of all unit moves
  perm = np.random.permutation(total_work)
  move_indices = move_indices[perm]
  move_signs = move_signs[perm]

  hyperspace = {}

  current = hv1.copy()

  prev_work = 0
  hyperspace[0] = current.copy()

  for level in range(1, levels):
    target_work = round(level * total_work / (levels - 1))

    n_new = target_work - prev_work

    if n_new > 0:
      batch_idx = move_indices[prev_work:target_work]
      batch_sign = move_signs[prev_work:target_work]

      np.add.at(current, batch_idx, batch_sign)

    hyperspace[level] = current.copy()
    prev_work = target_work

  return hyperspace



img_shoes = embed(cv2.imread('./images/shoes.jpg', cv2.IMREAD_GRAYSCALE))
img_pen = embed(cv2.imread('./images/pen.jpg', cv2.IMREAD_GRAYSCALE))
img_noise = embed(cv2.imread('./images/noise.jpg', cv2.IMREAD_GRAYSCALE))

vec_shoes = img_shoes.flatten().astype(np.int16)
vec_pen = img_pen.flatten().astype(np.int16)
levels = make_levels_manhattan(10, vec_shoes, vec_pen)
for idx in range(len(levels)):
  cv2.imwrite(f'./output/levels/shoes_to_pen_{idx:03d}_embed.jpg', levels[idx].reshape((512, 512)))

vec_pen = img_pen.flatten().astype(np.int16)
vec_noise = img_noise.flatten().astype(np.int16)
levels = make_levels_manhattan(10, vec_pen, vec_noise)
for idx in range(len(levels)):
  cv2.imwrite(f'./output/levels/pen_to_noise_{idx:03d}_embed.jpg', levels[idx].reshape((512, 512)))
