import numpy as np
from numpy.linalg import norm
import random
import copy

def sim(hv1, hv2):
  if norm(hv1) == 0 or norm(hv2) == 0:
    return 0
  return abs(np.dot(hv1, hv2) / (norm(hv1) * norm(hv2)))

def permute(hv, positions=[0,1], segments=1):
  hv = hv.reshape(segments, len(hv)//segments)
  hv = np.roll(hv, positions, axis=(0, 1))
  return np.ravel(hv)

def hv(n=10_000):
  return np.random.choice([1, -1], size=n)

def partial_permute(hv, pct=0.75):
  '''Random pair-wise swaps of hv elements'''
  n = len(hv)
  target_changes = int(np.ceil(pct * n))
  swaps = set()
  result = hv.copy()
  if target_changes < 2:
    return result, swaps

  for x in range(0, target_changes, 2):
    i, j = random.sample(range(n), 2)
    # swap the pair of element without inspecting their values
    result[i], result[j] = result[j], result[i]
    swaps.add((i, j))

  return result, swaps



dims = 10000

print('shift right 1 time')
hv = hv(n=dims)
hv_permuted1 = permute(hv)
print(hv, hv_permuted1)
print('sim', sim(hv, hv_permuted1))
print()

# swapping 100% of the elements doesß
#  not result in dissimilar hv. my guess is because
#  some of the pairs have the same values
print('swap 100% of the elements')
hv_1, swaps = partial_permute(hv, 1.00)
print(hv_1, len(swaps)*2)
print('sim', sim(hv, hv_1))
print()

print('swap 75% of the elements')
hv_75, swaps = partial_permute(hv, 0.75)
print(hv_75, len(swaps)*2)
print('sim', sim(hv, hv_75))
print()

print('swap 50% of the elements')
hv_50, swaps = partial_permute(hv, 0.50)
print(hv_50, len(swaps)*2)
print('sim', sim(hv, hv_50))
print()

print('swap 25% of the elements')
hv_25, swaps = partial_permute(hv, 0.25)
print(hv_25, len(swaps)*2)
print('sim', sim(hv, hv_25))
print()

print('swap 0% of the elements')
hv_0, swaps = partial_permute(hv, 0.00)
print(hv_0, len(swaps)*2)
print('sim', sim(hv, hv_0))
print()

