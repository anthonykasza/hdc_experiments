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

def partial_ordered_pairs_permute(hv, pct=0.75):
  '''Ordered pair-wise swaps of hv elements'''
  n = len(hv)
  target_changes = int(np.ceil(pct * n))
  swaps = set()
  result = hv.copy()
  if target_changes < 2:
    return result, swaps

  for x in range(0, target_changes, 2):
    result[x], result[x+1] = result[x+1], result[x]
    swaps.add((x, x+1))

  return result, swaps


def partial_random_pairs_permute(hv, pct=0.75):
  '''Random pair-wise swaps of hv elements'''
  target_changes = int(len(hv) * pct)
  unchanged = set(list(range(len(hv))))
  changed = set()
  swaps = set()
  result = hv.copy()

  while len(changed) < target_changes:
    i, j = random.sample(list(unchanged), 2)

    # swaps remind me of rc4
    result[i], result[j] = result[j], result[i]

    swaps.add((i, j))
    changed.add(i)
    changed.add(j)
    unchanged.remove(i)
    unchanged.remove(j)

  return result, swaps
