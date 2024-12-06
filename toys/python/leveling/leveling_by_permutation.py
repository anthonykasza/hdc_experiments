import numpy as np
import copy
from numpy.linalg import norm


def cossim(hdv1, hdv2):
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))

def new_hv(n):
  return np.random.choice([5,4,3,2,1, -1,-2,-3,-4,-5], size=n)

def permute(hdv, positions=[0,1], segments=1):
  hdv = hdv.reshape(segments, len(hdv)//segments)
  hdv = np.roll(hdv, positions, axis=(0, 1))
  return np.ravel(hdv)

def make_levels_by_permutation(count_of_levels=10, n=10_000):
  levels = []
  levels.append(new_hv(n))
  altered_indices = set([])
  elements_to_alter_per_iteration = n // count_of_levels

  for i in range(1, count_of_levels):
    next_level = copy.deepcopy(levels[i-1])
    block = next_level[(i-1) * elements_to_alter_per_iteration : elements_to_alter_per_iteration * i]
    block = permute(block)
    next_level[(i-1) * elements_to_alter_per_iteration : elements_to_alter_per_iteration * i] = block
    levels.append(next_level)
  return levels

# 10 dimensions, 5 levels, 2 elements permuted per level
levels = make_levels_by_permutation(count_of_levels=5, n=10)
for idx in range(len(levels)):
  level = levels[idx]
  if idx == 0:
    print(f'level0: {level}')
    continue
  print(f'level{idx}: {level}')
print()
print()

# 12 dimensions, 4 levels, 3 elements permuted per level
levels = make_levels_by_permutation(count_of_levels=4, n=12)
for idx in range(len(levels)):
  level = levels[idx]
  if idx == 0:
    print(f'level0: {level}')
    continue
  print(f'level{idx}: {level}')
print()
print()

# 10_000 dimensions, 100 levels, 100 elements permuted per level
levels = make_levels_by_permutation(count_of_levels=100, n=10_000)
for idx in range(len(levels)):
  level = levels[idx]
  if idx == 0:
    print(f'level0: {level}')
    continue
  print(f'level{idx}:  sim_to_{idx-1}: {cossim(levels[idx-1], level)},  sim_to_0: {cossim(levels[0], level)}')

