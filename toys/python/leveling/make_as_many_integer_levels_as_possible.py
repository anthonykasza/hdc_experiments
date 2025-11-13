
import copy
import numpy as np
from numpy.linalg import norm

def hdv(n=10_000, all=None, bound=100):
  '''generate a new integer hypervector'''
  if all is not None:
    return np.full((1, n), all).flatten()
  r = [x for x in range(-1*bound, bound+1) if x != 0]
  return np.random.choice(r, size=n)


def cossim(hdv1, hdv2):
  '''measure the similarity of 2 hypervector'''
  if norm(hdv1) == 0 or norm(hdv2) == 0:
    return 0
  return abs(np.dot(hdv1, hdv2) / (norm(hdv1) * norm(hdv2)))


def make_levels_incdec(hv1=hdv(), hv2=hdv(), i=1):
  '''return as many levels as possible'''
  levels = []
  levels.append(hv1)
  indices_to_alter = list(np.where(hv1 != hv2)[0])
  j = 0

  while not np.array_equal(levels[-1], hv2):
    # indices are chosen by round robin
    idx = indices_to_alter[j % len(indices_to_alter)]
    next_level = copy.deepcopy(levels[-1])

    # we need to increment
    if hv2[idx] > next_level[idx]:
      if hv2[idx] > next_level[idx] + i:
        next_level[idx] += i
      else:
        next_level[idx] = hv2[idx]
        indices_to_alter.remove(idx)
    # we need to decrement
    elif hv2[idx] < next_level[idx]:
      if hv2[idx] < next_level[idx] - i:
        next_level[idx] -= i
      else:
        next_level[idx] = hv2[idx]
        indices_to_alter.remove(idx)

    j += 1
    levels.append(next_level)
  return levels


hv1 = hdv(10)
hv2 = hdv(10)
print(f'hv1: {hv1}')
print(f'hv2: {hv2}')

levels = make_levels_incdec(hv1, hv2, 1)
for idx in range(len(levels)):
  level = levels[idx]
  sim = cossim(hv1, level)
  print(idx, level, sim)

  # TODO: investigate why this happens with some HV pairs
  if idx < len(levels)-1 and cossim(hv1, levels[idx+1]) > sim:
    print('  levels are becoming more similar instead of less similar')
